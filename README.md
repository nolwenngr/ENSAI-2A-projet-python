## Analyse de la fréquentation des musées en France entre 2001 et 2016

Par *Eulalie Amigo & Nolwenn Gorgé, ENSAI 2026*.

Les musées, en tant qu’institutions centrales de la diffusion du patrimoine et de la culture, sont des indicateurs sensibles des pratiques culturelles des populations, des politiques publiques en matière d’accès à la culture, et des évolutions sociétales plus larges. La période 2001-2016 est particulièrement intéressante car elle coïncide avec des réformes majeures, comme la loi de 2002 qui a redéfini le statut des musées en France, ainsi qu’avec des changements dans les comportements de visite (gratuités, diversification des publics, etc.). En effet, en 2001, les musées en France n’avaient pas encore l’appellation unique de « Musées de France ». Ils étaient classés en deux catégories : les musées « classés » (reconnus par l’État pour leur intérêt public) et les musées « contrôlés » (soumis à un contrôle scientifique et technique de l’État). Ces distinctions reflétaient une organisation héritée du XIXe siècle, avec des musées nationaux (comme le Louvre) et des musées locaux ou régionaux, souvent gérés par les collectivités. En janvier 2002, la loi relative aux musées de France est promulguée. Elle unifie le statut des musées en créant l’appellation « Musée de France », qui s’applique automatiquement aux musées nationaux et aux musées classés, puis aux musées contrôlés à partir de février 2003. Cette loi renforce les missions des musées : conservation, restauration, étude et diffusion des collections, mais aussi accès du plus grand nombre à la culture. Elle impose aussi des obligations en matière de gestion, de sécurité et de qualité des expositions, ce qui a pu influencer la fréquentation (meilleure attractivité, mais aussi parfois des fermetures temporaires pour mise aux normes).
Cependant, les observateurs économiques sont à l’unisson : tous constatent pour 2016 une chute du tourisme international en France de 7 %, et de 11 % si on se concentre sur la capitale. La cause ? Les attentats de janvier et novembre 2015 à Paris, ainsi que celui du 14 juillet 2016 à Nice.

Nous utiliserons les bases de données de la fréquentation des musées français entre  2001 et 2016 et du recensement des musées français du Ministère de la Culture.

# Problématique
Entre réformes institutionnelles (loi de 2002) et chocs conjoncturels (attentats de 2015-2016), comment les dynamiques spatiales et les caractéristiques propres aux musées permettent-elles d'expliquer les disparités de la fréquentation muséale en France ?

# Installation des dépendances nécessaires
Installez les dépendances nécessaires listées dans le fichier requirements.txt avec la commande `pip install -r requirements.txt`.

# Structure du projet
Le projet s'articule en trois parties. La première partie "nettoyage" importe les bases de données, unifie des noms de variables, analyse la non réponse totale et partielle et créer les variables utiles aux analyses suivantes. La seconde partie "réalise quelques analyses descriptives sur nos données notamment avec de la cartographie. Enfin, la troisième partie réalise un clustering. Les scripts sont présents dans le dossier "scripts". Le fichier "fonctions" répertorie des fonctions utilisées dans les scripts.

# Données utilisées

Ce projet s'appuie sur des données ouvertes (Open Data) publiques, principalement fournies par le Ministère de la Culture et hébergées sur la plateforme data.gouv.fr. 

L'analyse croise les trois jeux de données suivants :

* **[Entrées et catégories de public dans les musées](https://object.data.gouv.fr/ministere-culture/FREQ_MUSEES/ENTREES_ET_CATEGORIES_DE_PUBLIC.csv) (CSV)**
    * **Description :** Ce fichier détaille les entrées dans les établissements, ce qui permet d'analyser la fréquentation selon les différentes typologies de publics (gratuité, scolaires, etc.).
    * **Producteur :** Ministère de la Culture.

* **[Fréquentation totale des Musées de France 2001-2016](https://static.data.gouv.fr/resources/frequentation-des-musees-de-france-1/20250827-121955/frequentation-totale-mdf-2001-a-2016-data-def9.xlsx) (Excel)**
    * **Description :** Données retraçant l'évolution de la fréquentation globale des musées de France sur une période de 15 ans.
    * **Producteur :** Ministère de la Culture.

* **[Base Muséofile - Répertoire des musées de France](https://object.data.gouv.fr/ministere-culture/POP/museofile.csv) (CSV)**
    * **Description :** Le répertoire officiel contenant les métadonnées de chaque établissement ayant l'appellation "Musée de France" (identifiant unique, localisation géographique, domaines thématiques, statut juridique, etc.).
    * **Producteur :** Ministère de la Culture.