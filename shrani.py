import csv


def shrani(sez_podatkov):
    """Funkcija shrani podatke iz danega seznama podatkov v csv datoteko.
    Ustvari datoteke gore.csv, gore_okolica.csv in gore_poti.csv."""

    with open("gore.csv", "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(
            [
                "id",
                "ime",
                "država",
                "gorovje",
                "višina",
                "širina",
                "dolžina",
                "vrsta",
                "število ogledov",
                "priljubljenost",
                "mesto na lestvici priljubljenosti",
                "število slik",
                "število poti",
            ]
        )

        for podatek in sez_podatkov:
            pisatelj.writerow(
                [
                    podatek["id"],
                    podatek["ime"],
                    podatek["država"],
                    podatek["gorovje"],
                    podatek["višina"],
                    podatek["širina"],
                    podatek["dolžina"],
                    podatek["vrsta"],
                    podatek["število ogledov"],
                    podatek["priljubljenost"],
                    podatek["lestvica priljubljenosti"],
                    podatek["število slik"],
                    podatek["število poti"],
                ]
            )

    with open("gore_okolica.csv", "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["id", "id soseda"])
        for podatek in sez_podatkov:
            if podatek["gore v okolici 2km"] is not None:
                for gora in podatek["gore v okolici 2km"]:
                    pisatelj.writerow([podatek["id"], gora])

    with open("gore_poti.csv", "w", encoding="utf8") as dat:
        pisatelj = csv.writer(dat)
        pisatelj.writerow(["id", "začetna točka", "čas", "zahtevnost"])
        for podatek in sez_podatkov:
            if podatek["poti"] is not None:
                for pot in podatek["poti"]:
                    pisatelj.writerow([podatek["id"], pot[0], pot[1], pot[2]])
