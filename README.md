# Analiza vrhov iz hribi.net

Za projekt pri predmetu Uvod v programiranje sem si izbral analizo vrhov slovenskih gor in hribov, zbranih na spletni strani [Hribi.net](https://www.hribi.net/). Podatki so zbrani s pomočjo [iskalnika](https://www.hribi.net/iskalnik_izletov), kjer lahko izbereš državo in dobiš vse gore, ki so zbrane za to državo.

Za vsak vrh sem zajel:
- ime
- id
- državo
- gorovje
- višino (v metrih)
- geografsko širino in dolžino
- vrsto vrha (vrh, jezero, koča ...)
- število ogledov
- priljubljenost (v odstotkih)
- število slik
- število poti
- število GPS sledi
- opis
- druge gore, ki se nahajajo v okolici 2 km
- začetne točke poti, čas hoje in zahtevnost

Analiziral bom:
- slovenske gore, porazdeljenost vrhov, ločitev na gorovja
- poti
- priljubljenost vrhov

## Navodila  za uporabo

Uporabnik za pregled analize mora le odpreti dokument analiza.ipynb. 

Če hoče uporabnik sam zagnati program in si shraniti vse podatke, **zažene main.py**. Program main.py bo shranil vse spletne strani za države, ki so na voljo na Hribi.net ter nato še shranil vse gore in ostale lokacije za vse države. Program potrebuje nekaj časa, da vse shrani. Na koncu še shrani tri csv datoteke (gore.csv, gore_poti.csv in gore_okolica.csv), ki so uporabljene za analizo podatkov.

Ostali programi, torej zajem.py, izlusci.py ter shrani.py so pomožni programi, ki se izvedejo znotraj main.py.

Uporabljene knjižnice: os, re, requests, csv, pandas, matplotlib, plotly