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
    with open(path, 'w', encoding="utf-8") as f:
        f.write(text)

def save_page(url, directory, filename):
    """Funkcija shrani vsebino spletne strani iz "url" v datoteko "filename" v direktoriju
    "directory".
    """
    text = text_from_url(url)
    save_string_to_file(text, directory, filename)
    print(f"Uspešno shranil v {directory}/{filename}")

save_page(hribi_frontpage_url, hribi_directory, hribi_frontpage_filename) #shranimo vsebino spletne strani

def text_from_file(directory, filename):
    """Funkcija vrne besedilo iz datoteke "filename" v direktoriju "directory"."""
    path = os.path.join(directory, filename)
    with open(path, encoding="utf-8") as f:
        text = f.read()
    return text

def gorovja_iz_html(directory, filename):
    """Funkcija izlušči povezave do gorovij iz html datoteke "filename", po vzorcu iz hribi.net. Vrne seznam naborov oblike (povezava_do_gorovja, ime_gorovja)"""
    vzorec = r'<div class="vr\d"><a href="/gorovje(?P<link_gorovja>.*?)">(?P<ime_gorovja>.*?)</a></div>'
    return re.findall(vzorec, text_from_file(directory, filename))

for povezava, ime in gorovja_iz_html(hribi_directory, hribi_frontpage_filename):
    ime_datoteke = ime.lower().replace(",", "").replace(" ", "_") + ".html"
    link = 'https://hribi.net/gorovje' + povezava
    save_page(link, hribi_directory, ime_datoteke)
