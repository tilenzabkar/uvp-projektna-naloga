import os
import requests 
import re

hribi_url = 'https://www.hribi.net'
hribi_frontpage_url = 'https://www.hribi.net/gorovja'
hribi_directory = 'podatki'
hribi_frontpage_filename = 'gorovja.html'

def text_from_url(url):
    """Funkcija sprejme url spletne strani in poskusi vrniti vsebino spletne
    strani kot niz, v primeru napake vrne None.
    """
    try:
        page_content = requests.get(url)
    except requests.exceptions.RequestException:
        print("Spletna stran ni dosegljiva.")
        return None
    return page_content.text #samo besedilo

def save_string_to_file(text, directory, file):
    """Funkcija zapiše vrednost niza "text" v novo datoteko, ki se nahaja
    v "directory/filename", ali pa povozi obstoječo. V primeru, da je niz
    "directory" prazen, naredi datoteko v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True) #ustvarimo directory
    path = os.path.join(directory, file) #pot do datoteke
    with open(path, 'w', encoding="utf8") as f:
        f.write(text)

def save_page(url, directory, filename):
    """Funkcija shrani vsebino spletne strani iz "url" v datoteko "filename" v direktoriju
    "directory".
    """
    text = text_from_url(url)
    save_string_to_file(text, directory, filename)
    print(f"Uspešno shranil {directory}/{filename}")

save_page(hribi_frontpage_url, hribi_directory, hribi_frontpage_filename) #shranimo vsebino spletne strani

def text_from_file(directory, filename):
    """Funkcija vrne besedilo iz datoteke "filename" v direktoriju "directory"."""
    path = os.path.join(directory, filename)
    with open(path, encoding="utf8") as f:
        text = f.read()
    return text

def izlusci_gorovja_iz_html(directory, filename):
    """Funkcija izlušči povezave do gorovij iz html datoteke "filename", po vzorcu iz hribi.net. Vrne seznam naborov oblike (povezava_do_gorovja, ime_gorovja)"""
    vzorec = r'<div class="vr\d"><a href="/gorovje(?P<link_gorovja>.*?)">(?P<ime_gorovja>.*?)</a></div>'
    return re.findall(vzorec, text_from_file(directory, filename))

def shrani_gorovja_iz_html(directory, filename):
    """Funkcija shrani html vsebino gorovij v direktorije, ki imajo ime po gorovju, znotraj glavnega direktorija."""
    for povezava, ime in izlusci_gorovja_iz_html(directory, filename):
        nov_direktorij = ime.lower().replace(",", "").replace(" ", "_")
        pot = os.path.join(directory, nov_direktorij)
        os.makedirs(pot, exist_ok=True) 
        ime_html = nov_direktorij + ".html"
        link = 'https://hribi.net/gorovje' + povezava
        save_page(link, pot, ime_html)

shrani_gorovja_iz_html(hribi_directory, hribi_frontpage_filename) #shranimo spletne strani vseh gorovij

def izlusci_goro_iz_html(directory, filename):
    """Funkcija izlušči povezave do posameznih gor iz html datoteke "filename", ki se nahaja v direktoriju "directory". Vrne seznam povezav do nadaljnih spletnih strani
    posameznih vrhov."""
    vzorec = r'<tr class="vr\d"><td class="vrtd.*?"><a href="(?P<link_gore>.*?)">.*?</a></td>'
    return re.findall(vzorec, text_from_file(directory, filename))

def shrani_goro_iz_html(directory, filename):
    """Funkcija s pomočjo funkcije izlusci_goro_iz_html shrani html vsebino vsake posamezne gore v datoteko z naslovom gora{id}S.html."""
    mnozica_id = set()
    for povezava in izlusci_goro_iz_html(directory, filename):
        id = re.search(r'\d+/\d+', povezava).group(0).replace("/", "0") #vsaka gora je določena z vzorcem števke/števke, da dobimo id le zamenjamo / z 0 
        if id in mnozica_id:
            print("Podvojen id, napaka.")
            break
        mnozica_id.add(id)
        link = 'https://www.hribi.net' + povezava
        ime_datoteke = "gora" + id + ".html"
        save_page(link, directory, ime_datoteke)

def shrani_vse_vrhove(direktorij):
    """Funkcija shrani vse spletne strani posameznih vrhov iz direktorijev znotraj glavnega direktorija."""         
    for direktorij_znotraj in os.listdir(direktorij):
        pot = os.path.join(hribi_directory, direktorij_znotraj)
        if os.path.isdir(pot): #zanimajo nas le direktoriji
            for datoteka in os.listdir(pot):
                shrani_goro_iz_html(pot, datoteka)

shrani_vse_vrhove(hribi_directory)

