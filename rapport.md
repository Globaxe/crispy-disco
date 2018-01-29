## Compilateur - TP
### Introduction
Pour ce TP, nous avons choisi de développer un compilateur musical basé sur la librairie cSound.
Bien que flexible et puissante, cSound est une ancienne librairie qui possède une syntaxe plutôt compliquée : Avant d’écrire une partition, les instruments doivent d’abord être déclarés et leurs paramètres attribués. Côté partition, chaque note doit être déclarée “à la main”, sa durée et son temps de départ devant être spécifié.

```cSound

```
Notre but était donc de simplifier cette syntaxe, quitte à perdre un peu (beaucoup) de flexibilité.

### Partie métier

Le fichier utils.py s’occupe de la génération du code cSound. Toutes les méthodes concernant une génération de strings sont précédées du sucre “d_”
