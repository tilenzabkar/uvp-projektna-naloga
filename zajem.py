import os
import requests 
import re
import izlusci

hribi_glavni_url = r'https://www.hribi.net/iskalnik_izletov'
hribi_url = (r'https://www.hribi.net/iskalnik_izletov/rezultat_iskanja?drzavaid=1&gorovjeid=&'
             r'goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&'
             r'izhodisceMAX=&VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&'
             r'zahtevnostferrataid=&IzhodisceMinOddaljenost=&IzhodisceMAXOddaljenost=&'
             r'GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0')
hribi_directory = 'podatki'


def besedilo_iz_url(url):
    """Funkcija sprejme url spletne strani in poskusi vrniti vsebino spletne
    strani kot niz, v primeru napake ali preusmeritve vrne None."""

    try:
        page_content = requests.get(url, allow_redirects=False)
        if page_content.status_code == 302:  # gorovja nekaterih držav so bila premaknjena
            return None
    except requests.exceptions.RequestException:
        print("Spletna stran ni dosegljiva.")
        return None
    return page_content.text  # samo besedilo


def shrani_besedilo_v_datoteko(text, directory, file):
    """Funkcija zapiše vrednost niza "text" v novo datoteko, ki se nahaja
    v "directory/filename", ali pa povozi obstoječo."""

    os.makedirs(directory, exist_ok=True)  # ustvarimo directory
    path = os.path.join(directory, file)  # pot do datoteke
    with open(path, 'w', encoding="utf8") as f:
        f.write(text)


def shrani_stran(url, directory, filename):
    """Funkcija shrani vsebino spletne strani iz "url" v datoteko "filename" v direktoriju
    "directory"."""

    text = besedilo_iz_url(url)
    if text is not None:
        shrani_besedilo_v_datoteko(text, directory, filename)
        print(f"Uspešno shranil {filename}")


def besedilo_iz_datoteke(directory, filename):
    """Funkcija vrne besedilo iz datoteke "filename" v direktoriju "directory"."""

    path = os.path.join(directory, filename)
    with open(path, encoding="utf8") as f:
        text = f.read()
    return text


def shrani_vse_drzave(directory, sez_id_in_imen_drzav):
    """Funkcija shrani spletne strani vseh držav v direktorij "directory", ki
    za naprej vsebujejo povezave do gor. Sprejme tudi seznam podatkov o državah, 
    da ga ni potrebno večkrat računati."""

    for id, ime in sez_id_in_imen_drzav:
        ime_datoteke = ime.lower().replace(" ", "_") + ".html"
        shrani_stran((f'https://www.hribi.net/iskalnik_izletov/rezultat_iskanja?drzavaid={id}&gorovjeid=&'
                      'goraime=&VisinaMIN=&VisinaMAX=&CasMIN=&CasMAX=&izhodisce=&izhodisceMIN=&izhodisceMAX=&'
                      'VisinskaRazlikaMIN=&VisinskaRazlikaMAX=&zahtevnostid=&zahtevnostferrataid=&IzhodisceMinOddaljenost=&'
                      'IzhodisceMAXOddaljenost=&GoraMinOddaljenost=&GoraMaxOddaljenost=&mojaSirina=0&mojaDolzina=0'),
                     directory, ime_datoteke)


def shrani_gore_za_drzavo(filename):
    """Funkcija ustvari direktorij "gore" znotraj direktorija "podatki" in
    vanj shrani vse gore v obliki gora{id}.html. Podatke dobi iz programa
    izlusci.py, ki izlusci povezave do gorovij iz glavne strani."""

    direktorij_za_gore = 'gore'
    pot = os.path.join(hribi_directory, direktorij_za_gore)
    os.makedirs(pot, exist_ok=True)
    for povezava in izlusci.izlusci_gore(hribi_directory, filename):
        id = re.search(r'\d+/\d+', povezava).group(0).replace("/", "0")  # vsaka gora je določena z vzorcem števke/števke, da dobimo id le zamenjamo / z 0
        link = 'https://www.hribi.net' + povezava
        ime_datoteke = "gora" + id + ".html"
        shrani_stran(link, pot, ime_datoteke)


def shrani_gore_za_vse_drzave(sez_id_in_imen_drzav):
    """Funkcija z uporabo funkcije shrani_goro_iz_html(filename) shrani datoteke
    gor od vseh držav."""

    for id, ime in sez_id_in_imen_drzav:
        ime_datoteke = ime.lower().replace(" ", "_") + ".html"
        try:
            shrani_gore_za_drzavo(ime_datoteke)
        except FileNotFoundError:  # smo poskusili najti datoteko, za katero spletna stran ne obstaja in je zato nismo shranili
            print(f"Ni na voljo datoteke {ime_datoteke}.")
            continue


def zajemi_vse():
    """Funkcija pokliče vse potrebne funkcije, ki zajamejo potrebno
    vsebino za nadaljno analizo."""

    shrani_stran(hribi_glavni_url, hribi_directory, "glavni.html")
    sez_id_in_imen_drzav = izlusci.izlusci_id_drzav(hribi_directory, "glavni.html")
    shrani_vse_drzave(hribi_directory, sez_id_in_imen_drzav)
    shrani_gore_za_vse_drzave(sez_id_in_imen_drzav)