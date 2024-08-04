import zajem
import izlusci
import shrani

direktorij = 'podatki'

zajem.zajemi_vse(direktorij)

podatki = izlusci.izlusci_vrhove(direktorij)

shrani.shrani(podatki)