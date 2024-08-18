# Analiza vrhov iz hribi.net

Za projektno nalogo pri predmetu Uvod v programiranje sem si izbral analizo vrhov slovenskih in svetovnih gora in hribov, zbranih na spletni strani [Hribi.net](https://www.hribi.net/). Podatki so zbrani s pomočjo [iskalnika](https://www.hribi.net/iskalnik_izletov), kjer lahko izbereš državo in dobiš vse gore, ki so zbrane za to državo. Zbranih je 3318 vrhov in 9143 poti. 

Za vsak vrh sem zajel:
- ime,
- id,
- državo,
- gorovje,
- višino (v metrih),
- geografsko širino in dolžino,
- vrsto vrha (vrh, jezero, koča ...),
- število ogledov,
- priljubljenost (v odstotkih),
- število slik,
- število poti,
- druge gore, ki se nahajajo v okolici 2 km,
- začetne točke, čas hoje in zahtevnost poti za vsak vrh.

Analiziral bom:
- slovenske gore, porazdeljenost vrhov, ločitev na gorovja,
- poti,
- vplive na priljubljenost vrhov.

Spletna stran www.hribi.net je verjetno najbolj znana in s podatki obogatena spletna stran s hribovsko tematiko v Sloveniji. Kar 90 odstotkov opisov sta prispevala ustanovitelja, brata Rok in Tadej Lukan. [Vir](https://siol.net/sportal/naj-planinska-koca/brata-sta-zasnovala-spletno-stran-ki-vsakodnevno-resuje-ljubitelje-slovenskih-gora-505574) za nadaljne branje.

## Navodila  za uporabo

Uporabnik mora za pregled analize podatkov le odpreti dokument analiza.ipynb. V tem primeru bodo uporabljene csv datoteke iz repozitorija. Podatki so predstavljeni z Jupyter Notebook-om. 

Če hoče uporabnik sam zagnati program in si shraniti vse podatke, **zažene main.py**. Program main.py shrani spletne strani vseh držav in nato še vseh gora zbranih na pripadajočih spletnih straneh. Program potrebuje nekaj časa, da vse shrani. Potem, ko so podatki shranjeni, iz njih izlušči podatke za analizo in jih zapiše v csv datoteko. Ustvari tri csv datoteke, to so gore.csv, gore_poti.csv in gore_okolica.csv. Uporabnik si nato lahko ogleda analizo v analiza.ipynb.

Ostali programi, torej zajem.py, izlusci.py ter shrani.py so pomožni programi, ki se izvedejo znotraj main.py.

Uporabljene knjižnice: os, re, requests, csv, pandas, matplotlib, plotly.

Plotly je uporabljen le čisto na koncu analize kot plotly.express in je potreben za zagon interaktivnega zemljevida.