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


# --------------------------------------------------
# 2. Fonction principale de cartographie
# --------------------------------------------------
def carto_frequentation_region(
    df,
    annee,
    col_freq="frequentation",
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
