from cartiflette import carti_download
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata


def nettoyer_texte(serie):
    """
    Automatise la standardisation d'une série de chaîne de caractères.
    Cette fonction convertit les valeurs en chaînes de caractères, les met en
    majuscules, supprime les espaces en début et fin de chaîne, enlève les
    accents et autres signes.

    Parameters
    ----------
    serie : pandas.Series
        Série contenant les valeurs textuelles à standardiser.

    Returns
    -------
    pandas.Series
     """

    return (
        serie.astype(str)
        .str.upper()
        .str.strip()
        .apply(
            lambda x: unicodedata
            .normalize("NFKD", x)
            .encode("ascii", errors="ignore")
            .decode("utf-8")
        )
    )


def nettoyer_frequentation(df):
    """
    Nettoie la colonne de fréquentation d'un DataFrame :
    - Crée une colonne numérique 'freq_net'
    - Corrige la coquille sur 'appellation'

    Parameters
    ----------
    df : DataFrame
    Base de données que l'on veut nettoyer

    Return
    ------
    df_clean : DataFrame
    Base de données nettoyées
    """
    # On fait une copie
    df_clean = df.copy()

    # Création de la colonne numérique
    df_clean["freq_net"] = pd.to_numeric(df_clean["frequentation"], errors="coerce")

    # Correction de la coquille
    df_clean["frequentation"] = (
        df_clean["frequentation"]
        .replace("Retrait d'appelaltion", "Retrait d'appellation")
        )

    return df_clean


def ajouter_colonne_statut_precis(df):
    """
    Création de la colonne Statut.
    """
    df_copy = df.copy()
    # Dictionnaire des correspondances pour les valeurs non numériques
    statut = {
        "F": "Fermé",
        "NA": "NA",
        "NC": "NA",
        "Retrait d'appelaltion": "Retrait d'appellation",  # Corrige la coquille au passage
        "Retrait d'appellation": "Retrait d'appellation",
        "SO": "Sans Objet",
        "Transfert à Marseille - MUCEM": "Transfert",
        "Transfert à Nice": "Transfert"
    }

    # On applique le dictionnaire
    df_copy["Statut"] = df_copy["frequentation"].replace(statut)

    # On s'assure que les vraies valeurs vides (NaN) deviennent "NA"
    df_copy["Statut"] = df_copy["Statut"].fillna("NA")

    # Si la ligne a un chiffre valide dans freq_net, le statut devient "ouvert"
    df_copy.loc[df_copy["freq_net"].notna(), "Statut"] = "Ouvert"

    return df_copy


def tracer_comparaison_frequentation(bases_de_donnees, an='annee', freq='freq_net'):
    """
    Automatise la création de graphiques comparant la fréquentaion des musées
    par an en fonction du type de musée (payant, gratuit, total)

    Parameters
    ----------
    bases_de_donnees : dictionnaire
    dictionnaire contenant en valeur les base de données

    an : int
    Pour que faire les manipulations panda nom de la colonne année

    freq : int
    idem, ici c'est frequentation
    """
    # On parcourt notre dictionnaire pour tracer chaque courbe
    for nom_courbe, df in bases_de_donnees.items():

        # Pour les analyses descriptives on ne gadre que les musées ouverts
        df_propre = df[df['Statut'] == 'Ouvert']

        # On étudie la fréquentation totale, par an
        freq_annee = df_propre.groupby(an)[freq].sum()
        freq_annee.index = freq_annee.index.astype(int)

        # On trace la courbe
        plt.plot(freq_annee.index, freq_annee, marker='o', linewidth=2, label=nom_courbe)

    plt.title('Comparaison des évolutions des fréquentations', fontsize=14, fontweight='bold')
    plt.xlabel('Année', fontsize=12)
    plt.ylabel('Fréquentation', fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.7)

    # On affiche les année à 45°
    plt.xticks(freq_annee.index, rotation=45)

    # la légende
    plt.legend(title='Types de données', fontsize=11)
    plt.show()


def generer_carte_musees(df_donnees, an):
    """
    Prend en entrée un DataFrame contenant les musées et affiche
    directement la carte choroplèthe par région, avec le nombre de musées affiché.

    Parameters
    ----------
    df : pandas.DataFrame
        Table contenant les données de fréquentation. Elle doit inclure au moins :
        - une colonne de nom de région (NOMREG)
        - une colonne de référence du musée (REF DU MUSEE)
    an : str
        Année pour laquelle on souhaite faire la carte
    """
    # Selection de l'année
    df_donnees = df_donnees[df_donnees['annee'] == an]

    # Agrégation des données
    nb_musees_reg = (
        df_donnees
        .groupby("NOMREG", as_index=False)["REF DU MUSEE"]
        .nunique()
    )
    nb_musees_reg = nb_musees_reg.rename(columns={"REF DU MUSEE": "nb_musees"})

    # Téléchargement du fond de carte
    regions = carti_download(
        values=["France"],
        crs=4326,
        borders="REGION",
        vectorfile_format="geojson",
        simplification=50,
        filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022
    )

    # Nettoyage des textes et jointure
    nb_musees_reg["REGION_CLEAN"] = nettoyer_texte(nb_musees_reg['NOMREG'])
    regions["REGION_CLEAN"] = nettoyer_texte(regions["LIBELLE_REGION"])
    carte = regions.merge(nb_musees_reg, on="REGION_CLEAN", how="left")
    carte['nb_musees'] = carte['nb_musees'].fillna(0)

    # Création et affichage de la carte
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))

    carte.plot(
        column="nb_musees",
        ax=ax,
        cmap="OrRd",
        edgecolor="black",
        linewidth=0.8,
        legend=True,
        legend_kwds={
            'label': "Nombre de musées",
            'orientation': "vertical",
            'shrink': 0.7
        }
    )

    # Ajout du nombre de musées sur la carte
    for idx, row in carte.iterrows():
        if row.geometry is not None:
            point = row.geometry.representative_point()

            # On récupère le nombre

            valeur = int(row['nb_musees'])
            # On ajoute le texte sur la carte
            ax.annotate(
                text=str(valeur),
                xy=(point.x, point.y),
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=10,
                fontweight='bold',
                color='black'
            )

    plt.title("Répartition des musées par région", fontsize=16, fontweight='bold')
    plt.axis("off")

    # Affichage final
    plt.show()


def carto_frequentation_region(
    df,
    annee,
    col_freq="freq_net",
    col_region="NOMREG",
    col_annee="annee",
    cmap="OrRd",
    figsize=(10, 10)
):

    """
    Représente une carte de la France métropolitaine montrant la fréquentation
    agrégée par région pour une année donnée, classée en quartiles.

    Parameters
    ----------
    df : pandas.DataFrame
        Table contenant les données de fréquentation. Elle doit inclure au moins :
        - une colonne d'année
        - une colonne de nom de région
        - une colonne de fréquentation

    annee : int ou str
        Année à représenter sur la carte.

    col_freq : str, default="freq_net"
        Nom de la colonne contenant la fréquentation à agréger.

    col_region : str, default="NOMREG"
        Nom de la colonne contenant les noms des régions dans df.

    col_annee : str, default="annee"
        Nom de la colonne contenant l'année dans df.

    cmap : str, default="OrRd"
        Palette de couleurs utilisée pour la représentation cartographique.

    figsize : tuple, default=(10, 10)
        Taille de la figure matplotlib, sous la forme `(largeur, hauteur)`.

    Returns
    -------
    geopandas.GeoDataFrame
        GeoDataFrame issu de la jointure entre le fond de carte des régions et les
        données agrégées de fréquentation.
    """

    # Télécharger le fond de carte des régions
    regions = carti_download(
        values=["France"],
        crs=4326,
        borders="REGION",
        vectorfile_format="geojson",
        simplification=50,
        filter_by="FRANCE_ENTIERE_DROM_RAPPROCHES",
        source="EXPRESS-COG-CARTO-TERRITOIRE",
        year=2022
    )

    # Copie des données
    data = df.copy()

    # Filtrer l'année choisie
    data = data[data[col_annee] == annee].copy()

    # Convertir la fréquentation en numérique
    data[col_freq] = pd.to_numeric(data[col_freq], errors="coerce")

    # Agréger la fréquentation par région
    freq_region = (
        data.groupby(col_region, as_index=False)[col_freq]
        .sum()
    )

    # Nettoyer les noms de régions pour la jointure
    freq_region["REGION_CLEAN"] = nettoyer_texte(freq_region[col_region])

    col_region_carte = "LIBELLE_REGION"

    regions["REGION_CLEAN"] = nettoyer_texte(regions[col_region_carte])

    # Jointure entre les données et le fond de carte
    carte = regions.merge(freq_region, on="REGION_CLEAN", how="left")

    # Tracé de la carte
    fig, ax = plt.subplots(figsize=figsize)

    carte.plot(
        column=col_freq,
        cmap=cmap,
        linewidth=0.5,
        edgecolor="black",
        legend=True,
        scheme="quantiles",
        k=4,
        missing_kwds={"color": "lightgrey", "label": "Pas de données"},
        ax=ax
    )

    ax.set_title(f"Fréquentation des musées par région en ({annee})")
    ax.axis("off")
    plt.show()

    return carte
