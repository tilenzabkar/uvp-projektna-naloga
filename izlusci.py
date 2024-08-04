import re
import os

hribi_directory = 'podatki'

def text_from_file(directory, filename):
    """Funkcija vrne besedilo iz datoteke "filename" v direktoriju "directory"."""
    path = os.path.join(directory, filename)
    with open(path, encoding="utf8") as f:
        text = f.read()
    return text

def izlusci_vrhove(directory):
    """Funkcija izlušči podatke iz datotek gora{id}.html, znotraj direktorijev znotraj glavenga direktorija."""
    sez_podatkov = []
    for direktorij_znotraj in os.listdir(directory):
        pot = os.path.join(hribi_directory, direktorij_znotraj)
        if os.path.isdir(pot):
            for gora in os.listdir(pot):
              slovar_podatkov = {} 
              if re.search(r'\d', gora): #datoteke za gorovja, ki smo jih uporabili v zajem.py so v istem direktoriju in ne vsebujejo številk, nas ne zanimajo
                vsebina = text_from_file(pot, gora)
    	        
                #izluščimo ime
                vzorec_ime = r'<h1>(?P<ime>.+?)</h1>'
                najdba_ime = re.search(vzorec_ime, vsebina)
                if najdba_ime:
                    ime = najdba_ime.group('ime')
                    slovar_podatkov["ime"] = ime
                else:
                    print(f"Ime pri gori {gora} ni najdeno.")

                #izluščimo id
                vzorec_id = r'\d+'
                najdba_id = re.search(vzorec_id, gora)
                if najdba_id:
                    slovar_podatkov["id"] = najdba_id.group(0)
                else:
                    slovar_podatkov["id"] = None
                    print(f"Id pri gori {gora} ni najden.")

                #izluščimo gorovje
                vzorec_gorovje = r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".+?">(.+?)</a></div>'
                najdba_gorovje = re.search(vzorec_gorovje, vsebina)
                if najdba_gorovje:
                    slovar_podatkov["gorovje"] = najdba_gorovje.group(1)
                else:
                    slovar_podatkov["gorovje"] = None
                    print(f"Gorovje pri gori {gora} ni najdeno.")
                
                #izluščimo višino
                vzorec_višina = r'<div class="g2"><b>Višina:</b> (\d+?)&nbsp;(m)</div>'
                najdba_višina = re.search(vzorec_višina, vsebina)
                if najdba_višina:
                    slovar_podatkov["višina"] = najdba_višina.group(1) + najdba_višina.group(2)
                else:
                    slovar_podatkov["višina"] = None
                    print(f"Višina pri gori {gora} ni najdena.")

                #izluščimo geografsko širino in dolžino, nekateri tega 
                vzorec_sirina_dolzina = r'<div class="g2"><table><tr><td><b>Širina/Dolžina:</b>&nbsp;</td><td><span id="kf0">(?P<širina>.+?)&nbsp;(?P<dolžina>.+?)</span></td>.+?</tr></table></div>'
                najdba_sirina_dolzina = re.search(vzorec_sirina_dolzina, vsebina)
                if najdba_sirina_dolzina:
                    slovar_podatkov["širina/dolžina"] = najdba_sirina_dolzina.group("širina") + " " + najdba_sirina_dolzina.group("dolžina")   
                else:
                    #print(f"Geografska širina/dolžina pri gori {gora} ni najdena.") 
                    slovar_podatkov["širina/dolžina"] = None       

                #izluščimo vrsto
                vzorec_vrsta = r'<div class="g2"><b>Vrsta:</b> ?(.+?)</div>'
                najdba_vrsta = re.search(vzorec_vrsta, vsebina)
                if najdba_vrsta:
                    slovar_podatkov["vrsta"] = najdba_vrsta.group(1)
                else:
                    slovar_podatkov["vrsta"] = None
                    print(f"Vrsta pri gori {gora} ni bila najdena.")
                
                #izluščimo število ogledov
                vzorec_ogledi = r'<div class="g2"><b>Ogledov:</b> ?(.+?)</div>'
                najdba_ogledi = re.search(vzorec_ogledi, vsebina)
                if najdba_ogledi:
                    slovar_podatkov["število ogledov"] = najdba_ogledi.group(1)
                else:
                    slovar_podatkov["število ogledov"] = None
                    print(f"Število ogledov pri gori {gora} ni bilo najdeno.")
                
                #izluščimo priljubljenost
                vzorec_priljubljenost = r'<div class="g2"><b>Priljubljenost:</b> (.+?)&nbsp;\((.+?)&nbsp;mesto\)</div>'
                najdba_priljubljenost = re.search(vzorec_priljubljenost, vsebina)
                if najdba_priljubljenost:
                    slovar_podatkov["priljubljenost"] = najdba_priljubljenost.group(1)
                    slovar_podatkov["lestvica priljubljenosti"] = najdba_priljubljenost.group(2)
                else:
                    slovar_podatkov["priljubljenost"] = None
                    slovar_podatkov["lestvica priljubljenosti"] = None
                    print(f"Priljubljenost pri gori {gora} ni bila najdena.")
                
                #izluščimo število slik
                vzorec_slike = r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(.+?)</a></div>'
                najdba_slike = re.search(vzorec_slike, vsebina)
                if najdba_slike:
                    slovar_podatkov["število slik"] = najdba_slike.group(1)
                else:
                    slovar_podatkov["število slik"] = None
                    print(f"Število slik pri gori {gora} ni bilo najdeno.")

                #izluščimo število poti
                vzorec_st_poti = r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(.+?)</a></div>'
                najdba_st_poti = re.search(vzorec_st_poti, vsebina)
                if najdba_st_poti:
                    slovar_podatkov["število poti"] = najdba_st_poti.group(1)
                else:
                    slovar_podatkov["število poti"] = None
                    print(f"Število poti pri gori {gora} ni bilo najdeno.")

                #izluščimo število GPS sledi

                vzorec_gps = r'<div class="g2"><b>Število GPS sledi:</b> <a class="moder" href="/gps.asp" title="GPS sledi">(.+?)</a></div>'
                najdba_gps = re.search(vzorec_gps, vsebina)
                if najdba_gps:
                    slovar_podatkov["število GPS sledi"] = najdba_gps.group(1)
                else:
                    slovar_podatkov["število GPS sledi"] = None
                    print(f"Število GPS poti pri gori {gora} ni bilo najdeno.")
                
                #izluščimo opis

                vzorec_opis = r'<div style="padding-top:10px;"><b>Opis.*?:</b><br />(.+?)</div>'
                najdba_opis = re.search(vzorec_opis, vsebina, flags=re.DOTALL)
                if najdba_opis:
                    slovar_podatkov["opis"] = najdba_opis.group(1).replace("<br>", " ")
                else:
                    slovar_podatkov["opis"] = None
                    print(f"Opis pri gori {gora} ni bil najdeno.")

                sez_podatkov.append(slovar_podatkov)

                #izluščimo gore v okolici 2km

                vzorec_okolica = r'<div id="radiusseznam1">(.+?)</div>'
                najdba_okolica = re.search(vzorec_okolica, vsebina, flags=re.DOTALL)
                seznam_okoliskih_gor = []
                if najdba_okolica:
                    for okoliska_gora in re.finditer(r'<a class="moder" href=".+?">(.+?) \(\d+?m\)</a>', najdba_okolica.group(1), flags=re.DOTALL):
                        seznam_okoliskih_gor.append(okoliska_gora.group(1))
                    if len(seznam_okoliskih_gor) != 0:
                        slovar_podatkov["gore v okolici 2km"] = seznam_okoliskih_gor
                    else:
                        slovar_podatkov["gore v okolici 2km"] = None
                else:
                    slovar_podatkov["gore v okolici 2km"] = None
                    #print(f"Gore v okolici gore {gora} niso bile najdene.")

                #izluščimo začetne točke poti, čas hoje in zahtevnost

                vzorec_poti = r'<tr class="trG\d"><td class="tdG"><a href=".+?">(.+?) - .+?</a></td><td class="tdG"><a href=".+?"> ?(.+?)</a></td><td class="tdG"><a href=".+?">(.+?)</a></td></tr>'
                najdba_poti = re.findall(vzorec_poti, vsebina)
                if najdba_poti:
                    slovar_podatkov["poti"] = najdba_poti
                else:
                    slovar_podatkov["poti"] = None
                    #print(f"Pri gori {gora} ni bilo najdenih poti.")
                
    return sez_podatkov
        #izluščimo gore v okolici

        #izluščimo opis

        #izluščimo poti, potreben čas in zahtevnost

#print(sorted(izlusci_vrhove(hribi_directory), key=lambda x: int(x["lestvica priljubljenosti"][:-1])))
print(izlusci_vrhove(hribi_directory))