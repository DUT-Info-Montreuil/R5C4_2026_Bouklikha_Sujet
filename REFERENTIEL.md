# Référentiel de `parties.db`

Ce document donne les valeurs exactes présentes dans la base. Les filtres de
l'API utilisent le **code** du serveur et les libellés des jeux et des files.
Les comparaisons peuvent être rendues insensibles à la casse, mais les accents
font partie des noms affichés.

## Serveurs

| Code à utiliser | Nom | Région |
| --- | --- | --- |
| `EUW` | Europe West | Europe |
| `EUNE` | Europe Nordic & East | Europe |
| `NA` | North America | Americas |
| `KR` | Korea | Asia |
| `BR` | Brazil | Americas |
| `LAN` | Latin America North | Americas |

## Jeux et files

| Jeu à utiliser | Files associées |
| --- | --- |
| `LoL` | `Classée solo`, `Classée flexible`, `Normale draft`, `ARAM` |
| `Valorant` | `Compétitive`, `Non classée`, `Swiftplay` |
| `TFT` | `Classée`, `Normale`, `Double Up` |
| `Wild Rift` | `Classée`, `Normale` |
| `Legends of Runeterra` | `Classée`, `Normale` |

> Les noms `Classée` et `Normale` existent pour plusieurs jeux. Pour filtrer
> une file portant l'un de ces noms, il faut donc aussi préciser le jeu.

## Années disponibles

`2023`, `2024`, `2025`

Le même contenu est fourni en JSON par la future route
`GET /api/v1/parties/referentiel` et, à partir de la séance 3, dans
`fixtures/referentiel.json`.
