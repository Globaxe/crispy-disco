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
développer dans les tp du cours de compilateur.

Afin de gérer les notes sans trop se compliquer la vie nous avons utilisé une liste de notes à laquelle nous avons ajouté un chiffre de 1 à 9 correspondant à l'octave. Finalement nous utilisons la fonction `join()` pour créer une regexp facilement grace au décorateur `@TOKEN` car on ne peut pas le faire directement dans la docstring.

```python
notes = (
    'do',
    'do\#',
    're',
    're\#',
    'mi',
    'mi\#',
    'fa',
    'fa\#',
    'sol',
    'sol\#',
    'la',
    'la\#',
    'si',
    'si\#'
)

notes = [note+str(i) for note in notes for i in range(1,9)]

@TOKEN(r'|'.join(notes))
def t_NOTE(t):
    return t
```

Notre code ne possédant pas de marqueur de fin de ligne nous avons créé un un token `t_NEWLINE` qui permet de reconnaitre une ou plusieurs fin de lignes.

```python
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno+=len(t.value)
    return t
```

Nous avons aussi utilisé un token `t_comment` permettant de reconnaitre les commentaires sur une ligne commençant par `#`. Par contre, les commentaires multilignes ne sont pas implémentés.

```python
def t_comment(t):
    r'\#.*\n*'
    t.lexer.lineno+=t.value.count('\n')
 ```

### Parseur

todo

### Syntaxe

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

Les classes suivantes sont également présente pour stocker les réglages, notes et accords déclarés :

```python
class Settings():
    def __init__(self):
        self.bpm = 120
        self.dt = 0.5

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.dt = 60/self.bpm

class Note():
    def __init__(self, key, octave):
        self.key = key
        self.octave = octave

class Chord():
    def __init__(self, notes):
        self.notes = notes
```

les fonctions principales sont les suivantes :

```python

''' Fonctionnel '''
# Ajoute un instrument. Types disponibles : sine, square, saw, pulse
def add_instr(name, type):
  # ...

# Force un instrument à faire une pause spécifiée par le paramètre dur
def wait(instrName, dur):
  # ...

''' Génération de string '''
# Retourne un string comportant la déclaration de base d'une partition cSound.
def d_starting():

# Retourne un string comportant la déclaration de tous les
# instruments précédemments déclarés, ainsi que leur type.
# Doit être appellée au début du fichier.
def d_instruments():
  # ...

# Retourne un string comportant la déclaration d'une note unique.
# Les paramètres a, d, s, r ne sont pour l'instant
# pas utilisés mais définissent la forme d'onde d'une note.
# le paramètre chord est utilisé pour évité l'incrémentation
# de l'offset d'un instrument lors de la création d'accords.
def d_note(instrName, dur, amp, note, a, d, s, r, sta=None, chord=False):
  # ...

# Déclare un accord, soit n notes déclenchées au même moment par un
# même instrument.
def d_chord(instrName, dur, amp, chord, a, d, s, r, sta=None):
  # ...

# Retoure un string déclarant un arpège : Répète un accord sur
# plusieurs octaves avec une durée de note constante.
# Le sens (montant / descendant) peut être spécifié par la variable inc (-1 / 1)
def d_arp(instrName, dur, amp, chord, a, d, s, r, loops, inc, sta = None):
  # ...

# Retourne le string terminant la déclaration d'une partition cSound.
def d_end():
  #...
```
