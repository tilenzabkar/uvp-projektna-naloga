import re
import os

hribi_directory = 'podatki'


def besedilo_iz_datoteke(directory, filename):
    """Funkcija vrne besedilo iz datoteke "filename" v direktoriju "directory"."""

    path = os.path.join(directory, filename)
    with open(path, encoding="utf8") as f:
        text = f.read()
    return text


def izlusci_gore(directory, filename):
    """Funkcija izlušči povezave do gorovij iz vsebine datoteke "filename" v direktoriju "directory" po vzorcu iz hribi.net."""

    vzorec = r'<tr class="naslov2"><td class="tdG0" colspan="2"><a href="(?P<link>.+?)"><b>.+?</b></a></td></tr>'
    return re.findall(vzorec, besedilo_iz_datoteke(directory, filename))


def izlusci_id_drzav(directory, filename):
    """Funkcija izlušči id držav iz datoteke "filename" iz direktorija "directory" in vrne seznam naborov (id, ime)."""

    vzorec = r'<select name="drzavaid" class="select" onchange="prikazigorovja\(parseInt\(this.value\)\);">.+?</select>'
    najdba = re.search(vzorec, besedilo_iz_datoteke(directory, filename), flags=re.DOTALL)
    sez = []
    for id in re.finditer(r'option value="(\d+)">(.+?)</option>', najdba.group(0)):
        sez.append((id.group(1), id.group(2)))
    return sez


def izlusci_vrhove(directory):
    """Funkcija izlušči podatke iz datoteke gora{id}.html, znotraj direktorijev znotraj glavenga direktorija."""

    sez_podatkov = []
    pot = os.path.join(hribi_directory, directory)
    for gora in os.listdir(pot):
        slovar_podatkov = {}
        vsebina = besedilo_iz_datoteke(pot, gora)

        # izluščimo ime
        vzorec_ime = r'<h1>(?P<ime>.+?)</h1>'
        najdba_ime = re.search(vzorec_ime, vsebina)
        if najdba_ime is not None:
            ime = najdba_ime.group('ime')
            slovar_podatkov["ime"] = ime
        else:
            slovar_podatkov["ime"] = None
            print(f"Ime pri gori {gora} ni najdeno.")

        # izluščimo id
        vzorec_id = r'\d+'
        najdba_id = re.search(vzorec_id, gora)
        if najdba_id is not None:
            slovar_podatkov["id"] = najdba_id.group(0)
        else:
            slovar_podatkov["id"] = None
            print(f"Id pri gori {gora} ni najden.")

        # izluščimo državo
        sez_drzav = []
        vzorec_drzave = r'<div class="g2"><b>Država:</b> (<a class="moder" href=".+?">.+?</a>)+?</div>'
        najdba_drzave = re.search(vzorec_drzave, vsebina, flags=re.DOTALL)
        if najdba_drzave is not None:
            for drzava in re.finditer(r'">(.+?)</a>', najdba_drzave.group(1), flags=re.DOTALL):
                sez_drzav.append(drzava.group(1))
            slovar_podatkov["država"] = ", ".join(sez_drzav)
        else:
            slovar_podatkov["država"] = None
            print(f"Država pri gori {gora} ni bila najdena.")

        # izluščimo gorovje
        vzorec_gorovje = r'<div class="g2"><b>Gorovje:</b> <a class="moder" href=".+?">(.+?)</a></div>'
        najdba_gorovje = re.search(vzorec_gorovje, vsebina)
        if najdba_gorovje is not None:
            slovar_podatkov["gorovje"] = najdba_gorovje.group(1)
        else:
            slovar_podatkov["gorovje"] = None
            print(f"Gorovje pri gori {gora} ni najdeno.")

        # izluščimo višino
        vzorec_višina = r'<div class="g2"><b>Višina:</b> (\d+?)&nbsp;m</div>'
        najdba_višina = re.search(vzorec_višina, vsebina)
        if najdba_višina is not None:
            slovar_podatkov["višina"] = najdba_višina.group(1)
        else:
            slovar_podatkov["višina"] = None
            print(f"Višina pri gori {gora} ni najdena.")

        # izluščimo geografsko širino in dolžino
        vzorec_sirina_dolzina = (r'<div class="g2"><table><tr><td><b>Širina/Dolžina:</b>&nbsp;</td><td><span id="kf0">(?P<širina>.+?)'
                                 r'&nbsp;(?P<dolžina>.+?)</span></td>.+?</tr></table></div>')
        najdba_sirina_dolzina = re.search(vzorec_sirina_dolzina, vsebina)
        if najdba_sirina_dolzina is not None:
            slovar_podatkov["širina"] = najdba_sirina_dolzina.group("širina").replace(",", ".").replace("°N", "")
            slovar_podatkov["dolžina"] = najdba_sirina_dolzina.group("dolžina").replace(",", ".").replace("°E", "")
        else:
            slovar_podatkov["širina"] = None
            slovar_podatkov["dolžina"] = None

        # izluščimo vrsto
        vzorec_vrsta = r'<div class="g2"><b>Vrsta:</b> ?(.+?)</div>'
        najdba_vrsta = re.search(vzorec_vrsta, vsebina)
        if najdba_vrsta is not None:
            slovar_podatkov["vrsta"] = najdba_vrsta.group(1)
        else:
            slovar_podatkov["vrsta"] = None
            print(f"Vrsta pri gori {gora} ni bila najdena.")

        # izluščimo število ogledov
        vzorec_ogledi = r'<div class="g2"><b>Ogledov:</b> ?(.+?)</div>'
        najdba_ogledi = re.search(vzorec_ogledi, vsebina)
        if najdba_ogledi is not None:
            slovar_podatkov["število ogledov"] = najdba_ogledi.group(1).replace(".", "")
        else:
            slovar_podatkov["število ogledov"] = None
            print(f"Število ogledov pri gori {gora} ni bilo najdeno.")

        # izluščimo priljubljenost
        vzorec_priljubljenost = r'<div class="g2"><b>Priljubljenost:</b> (.+?)%&nbsp;\((.+?)&nbsp;mesto\)</div>'
        najdba_priljubljenost = re.search(vzorec_priljubljenost, vsebina)
        if najdba_priljubljenost is not None:
            slovar_podatkov["priljubljenost"] = najdba_priljubljenost.group(1)
            slovar_podatkov["lestvica priljubljenosti"] = najdba_priljubljenost.group(2)
        else:
            slovar_podatkov["priljubljenost"] = None
            slovar_podatkov["lestvica priljubljenosti"] = None
            print(f"Priljubljenost pri gori {gora} ni bila najdena.")

        # izluščimo število slik
        vzorec_slike = r'<div class="g2"><b>Število slik:</b> <a class="moder" href="#slike">(.+?)</a></div>'
        najdba_slike = re.search(vzorec_slike, vsebina)
        if najdba_slike is not None:
            slovar_podatkov["število slik"] = najdba_slike.group(1)
        else:
            slovar_podatkov["število slik"] = None
            print(f"Število slik pri gori {gora} ni bilo najdeno.")

        # izluščimo število poti
        vzorec_st_poti = r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(.+?)</a></div>'
        najdba_st_poti = re.search(vzorec_st_poti, vsebina)
        if najdba_st_poti is not None:
            slovar_podatkov["število poti"] = najdba_st_poti.group(1)
        else:
            slovar_podatkov["število poti"] = None
            print(f"Število poti pri gori {gora} ni bilo najdeno.")

        # izluščimo gore v okolici 2km
        vzorec_okolica = r'<div id="radiusseznam1">(.+?)</div>'
        najdba_okolica = re.search(vzorec_okolica, vsebina, flags=re.DOTALL)
        seznam_okoliskih_gor = []
        if najdba_okolica is not None:
            for okoliska_gora in re.finditer(r'<a class="moder" href="/gora/.+?/(\d+/\d+)">.+? \(\d+?m\)</a>', najdba_okolica.group(1), flags=re.DOTALL):
                id = okoliska_gora.group(1).replace("/", "0")
                seznam_okoliskih_gor.append(id)
            if len(seznam_okoliskih_gor) != 0:
                slovar_podatkov["gore v okolici 2km"] = seznam_okoliskih_gor
            else:
                slovar_podatkov["gore v okolici 2km"] = None
        else:
            slovar_podatkov["gore v okolici 2km"] = None

        # izluščimo začetne točke poti, čas hoje in zahtevnost
        vzorec_poti = (r'<tr class="trG\d"><td class="tdG"><a href=".+?"> ?(.+?) ?[-\(].+?</a></td><td class="tdG"><a href=".+?">'
                       r' ?(.+?)</a></td><td class="tdG"><a href=".+?">(.+?)</a></td></tr>')
        najdba_poti = re.findall(vzorec_poti, vsebina)
        if najdba_poti is not None:
            slovar_podatkov["poti"] = najdba_poti
        else:
            slovar_podatkov["poti"] = None
        sez_podatkov.append(slovar_podatkov)
    return sez_podatkov
