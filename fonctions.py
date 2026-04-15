from cartiflette import carti_download
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata


# --------------------------------------------------
# 1. Fonction pour nettoyer les noms de régions
# --------------------------------------------------
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


# --------------------------------------------------------------
# 2.Fonction pour automatiser la création d'une colonne "Statut"
# --------------------------------------------------------------
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

# -----------------------------------------
# 3.Fonction pour la création de graphique comparant
# les féquentations de de musées en fonction de type de musée
# ----------------------------------------


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

    an : int
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


# --------------------------------------------------
# 4. Fonction principale de cartographie
# --------------------------------------------------
def carto_frequentation_region(
    df,
    annee,
    col_freq="freq_net",
    col_region="NOMREG",
    col_annee="annee",
    cmap="OrRd",
    figsize=(10, 10)
):
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
