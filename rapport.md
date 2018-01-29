## Compilateur - TP

#### Cédric Pahud, Guillaume Noguera

##### *INF3-dlma*

### Introduction
Pour ce TP, nous avons choisi de développer un compilateur musical basé sur la librairie cSound.
Bien que flexible et puissante, cSound est une ancienne librairie qui possède une syntaxe plutôt compliquée : Avant d’écrire une partition, les instruments doivent d’abord être déclarés et leurs paramètres attribués. Côté partition, chaque note doit être déclarée “à la main”, sa durée et son temps de départ devant être spécifié.

Notre but était donc de simplifier cette syntaxe, quitte à perdre un peu (beaucoup) de flexibilité.

Exemple cSound :

```python
<CsoundSynthesizer>
# Options de sortie
<CsOptions>
-odac
-o out.wav _W
</CsOptions>

# Déclaration d'un instrument et binding des paramètres
<CsInstruments>
sr=44100
ksmps=10
nchnls=1
instr 1
iamp=p4
ifreq=cpspch(p5)
iatt=p6
idec=p7
islev=p8
irel=p9
kenv adsr p3/iatt, p3/idec, islev, p3/irel
aout oscil iamp*kenv, ifreq, 1
out aout
endin
</CsInstruments>

<CsScore>
# Déclaration de la forme d'onde
f1 0 16384 10 1 0.5 0.3 0.25 0.2 0.167 0.14 0.125 .111
# Début de la partition
i 1 1.50 1.50 10000.00 5.09 1.00 6.00 1.00 1.50
i 1 3.00 1.50 10000.00 6.09 1.00 6.00 1.00 1.50
i ...
```

### Analyseur lexical

Pour développer l'Analyseur lexical nous nous sommes basé sur le fichier lex5.py
développer dans les tp du cours de compilateur

### Parseur

todo

### Partie métier

Le fichier utils.py s’occupe de la génération du code cSound. Toutes les méthodes concernant une génération de strings sont précédées du sucre syntaxique “d_<function>”

Il s'occupe de gérer les instruments ainsi que leurs offsets, notre compilateur fonctionnant en mode "note à note" (cSound attendant de nous de spécifier le temps de départ de chaque note):

```python
class Instrument():
    def __init__(self, id, type):
        self.id = id
        self.type = type
        self.offset = 0
```

à chaque fois qu'un instrument joue une note, son offset est augmenté.
les trois fonctions principales sont les suivantes :

```python
# Retourne un string comportant la déclaration de tous les instruments précédemments déclarés, ainsi que leur type
def d_instruments():
  # ...

# Retourne un string comportant la déclaration d'une note unique.
# Les paramètres a, d, s, r ne sont pour l'instant pas utilisés mais définissent la
# forme d'onde d'une note.
# le paramètre chord est utilisé pour évité l'incrémentation de l'offset d'un
# instrument lors de la création d'accords.
def d_note(instrName, dur, amp, note, a, d, s, r, sta=None, chord=False):
  # ...
```
