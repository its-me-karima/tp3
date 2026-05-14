import numpy as np
import random
import csv
import pickle


# =========================================================
# CLASSE ENREGISTREMENT
# =========================================================
class Enregistrement:

    def __init__(self, temperature, humidite, precipitations,
                 vent, pression, indice_uv):

        self.__temperature = temperature
        self.__humidite = humidite
        self.__precipitations = precipitations
        self.__vent = vent
        self.__pression = pression
        self.__indice_uv = indice_uv

    # ================= GETTERS =================
    def getTemperature(self):
        return self.__temperature

    def getHumidite(self):
        return self.__humidite

    def getPrecipitations(self):
        return self.__precipitations

    def getVent(self):
        return self.__vent

    def getPression(self):
        return self.__pression

    def getIndiceUV(self):
        return self.__indice_uv

    # ================= SETTERS =================
    def setTemperature(self, value):
        self.__temperature = value

    def setHumidite(self, value):
        self.__humidite = value

    def setPrecipitations(self, value):
        self.__precipitations = value

    def setVent(self, value):
        self.__vent = value

    def setPression(self, value):
        self.__pression = value

    def setIndiceUV(self, value):
        self.__indice_uv = value

    # =========================================================
    # METHODE SCORE
    # =========================================================
    def score(self):

        valeurs = [
            self.__temperature,
            self.__humidite,
            self.__precipitations,
            self.__vent,
            self.__indice_uv
        ]

        for v in valeurs:
            if np.isnan(v):
                return 0

        s = 0

        t = self.__temperature
        h = self.__humidite
        p = self.__precipitations
        v = self.__vent
        uv = self.__indice_uv

        # TEMPÉRATURE
        if 18 <= t <= 28:
            s += 25
        elif 10 <= t < 18 or 28 < t <= 32:
            s += 15
        else:
            s += 5

        # HUMIDITÉ
        if 40 <= h <= 70:
            s += 15
        elif 30 <= h < 40 or 70 < h <= 80:
            s += 8
        else:
            s += 3

        # PRÉCIPITATIONS
        if 0 <= p <= 2:
            s += 15
        elif 2 < p <= 10:
            s += 8
        else:
            s += 0

        # VENT
        if 0 <= v <= 30:
            s += 15
        elif 30 < v <= 60:
            s += 8
        else:
            s += 0

        # UV
        if 0 <= uv <= 5:
            s += 15
        elif uv <= 7:
            s += 8
        else:
            s += 2

        return s

    # =========================================================
    # AFFICHAGE
    # =========================================================
    def __str__(self):
        return (
            "Temp=" + str(self.__temperature) + "C | " +
            "Hum=" + str(self.__humidite) + "% | " +
            "Pluie=" + str(self.__precipitations) + "mm | " +
            "Vent=" + str(self.__vent) + "km/h | " +
            "Press=" + str(self.__pression) + "hPa | " +
            "UV=" + str(self.__indice_uv) + " | " +
            "Score=" + str(self.score())
        )


# =========================================================
# LISTE DES MOIS
# =========================================================
annee = [
    ("janvier", 31),
    ("fevrier", 29),
    ("mars", 31),
    ("avril", 30),
    ("mai", 31),
    ("juin", 30),
    ("juillet", 31),
    ("aout", 31),
    ("septembre", 30),
    ("octobre", 31),
    ("novembre", 30),
    ("decembre", 31)
]


# =========================================================
# CLASSE STATION
# =========================================================
class Station:

    def __init__(self, nom, localisation):

        self.__nom = nom
        self.__localisation = localisation
        self.__data = {}

        self.generer_donnees()

    # ================= GETTERS =================
    def getNom(self):
        return self.__nom

    def getLocalisation(self):
        return self.__localisation

    def getData(self):
        return self.__data

    # ================= SETTERS =================
    def setNom(self, value):
        self.__nom = value

    def setLocalisation(self, value):
        self.__localisation = value

    # =========================================================
    # GENERATION ALEATOIRE DES DONNEES
    # =========================================================
    def generer_donnees(self):

        for mois, jours in annee:

            self.__data[mois] = {}

            for jour in range(1, jours + 1):

                enregistrement = Enregistrement(
                    random.choice([np.nan, random.randint(0, 40)]),
                    random.choice([np.nan, random.randint(0, 100)]),
                    random.choice([np.nan, random.randint(0, 20)]),
                    random.choice([np.nan, random.randint(0, 100)]),
                    random.choice([np.nan, random.randint(980, 1040)]),
                    random.choice([np.nan, random.randint(0, 11)])
                )

                self.__data[mois][jour] = enregistrement

    # =========================================================
    # LISTE DES ENREGISTREMENTS
    # =========================================================
    def _liste_enregistrements(self, mois):
        return list(self.__data[mois].values())

    # =========================================================
    # TEMPERATURES UNIQUES
    # =========================================================
    def temperatures_uniques(self, mois):

        liste = []

        for e in self._liste_enregistrements(mois):

            t = e.getTemperature()

            if not np.isnan(t):
                liste.append(t)

        return list(set(liste))

    # =========================================================
    # TEMPERATURE MOYENNE
    # =========================================================
    def temperature_moyenne(self, mois):

        liste = []

        for e in self._liste_enregistrements(mois):

            t = e.getTemperature()

            if not np.isnan(t):
                liste.append(t)

        if len(liste) > 0:
            return round(sum(liste) / len(liste), 2)

        return np.nan

    # =========================================================
    # JOURS PLUVIEUX
    # =========================================================
    def jours_pluvieux(self, mois):

        jours = []

        for jour, e in self.__data[mois].items():

            p = e.getPrecipitations()

            if not np.isnan(p) and p > 0:
                jours.append(jour)

        return jours

    # =========================================================
    # JOURS EXTREMES
    # =========================================================
    def jours_extremes(self, mois):

        jours = []

        for jour, e in self.__data[mois].items():

            t = e.getTemperature()

            if not np.isnan(t) and (t < 5 or t > 35):
                jours.append(jour)

        return jours

    # =========================================================
    # HUMIDITE MOYENNE
    # =========================================================
    def humidite_moyenne(self, mois):

        liste = []

        for e in self._liste_enregistrements(mois):

            h = e.getHumidite()

            if not np.isnan(h):
                liste.append(h)

        if len(liste) > 0:
            return round(sum(liste) / len(liste), 2)

        return np.nan

    # =========================================================
    # PRECIPITATIONS TOTALES
    # =========================================================
    def precipitations_totales(self, mois):

        total = 0

        for e in self._liste_enregistrements(mois):

            p = e.getPrecipitations()

            if not np.isnan(p):
                total += p

        return round(total, 2)

    # =========================================================
    # JOURS BEAUX
    # =========================================================
    def jours_beaux(self, mois):

        jours = []

        for jour, e in self.__data[mois].items():

            if e.score() >= 80:
                jours.append(jour)

        return jours

    # =========================================================
    # SCORE MOYEN
    # =========================================================
    def score_moyen(self, mois):

        scores = []

        for e in self._liste_enregistrements(mois):
            scores.append(e.score())

        if len(scores) > 0:
            return round(sum(scores) / len(scores), 2)

        return 0

    # =========================================================
    # MOIS LE PLUS BEAU
    # =========================================================
    def mois_beau(self):

        meilleur_mois = None
        meilleur_score = -1

        for mois, _ in annee:

            s = self.score_moyen(mois)

            if s > meilleur_score:
                meilleur_score = s
                meilleur_mois = mois

        return meilleur_mois

    # =========================================================
    # EXPORT CSV
    # =========================================================
    def exporter_csv(self):

        nom_fichier = self.__nom + ".csv"

        with open(nom_fichier, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            writer.writerow([
                "nom_station",
                "mois",
                "jour",
                "temperature",
                "humidite",
                "precipitations",
                "vent",
                "pression",
                "indice_uv",
                "score"
            ])

            for mois, _ in annee:

                for jour, e in self.__data[mois].items():

                    writer.writerow([
                        self.__nom,
                        mois,
                        jour,
                        e.getTemperature(),
                        e.getHumidite(),
                        e.getPrecipitations(),
                        e.getVent(),
                        e.getPression(),
                        e.getIndiceUV(),
                        e.score()
                    ])

        print("CSV créé :", nom_fichier)

    # =========================================================
    # AFFICHAGE
    # =========================================================
    def __str__(self):
        return (
            "Station : " + self.__nom +
            " | Localisation : " + self.__localisation
        )


# =========================================================
# QUESTION 5
# CREATION DES STATIONS
# =========================================================
station_casa = Station("Station_Casa", "Casablanca")
station_rabat = Station("Station_Rabat", "Rabat")
station_fes = Station("Station_Fes", "Fes")
station_marrakech = Station("Station_Marrakech", "Marrakech")


# =========================================================
# TEST DES METHODES
# =========================================================
print("\n===== TESTS =====\n")

print(station_casa)

print("\nTemperature moyenne janvier :")
print(station_casa.temperature_moyenne("janvier"))

print("\nHumidite moyenne janvier :")
print(station_casa.humidite_moyenne("janvier"))

print("\nPrecipitations totales janvier :")
print(station_casa.precipitations_totales("janvier"))

print("\nJours pluvieux janvier :")
print(station_casa.jours_pluvieux("janvier"))

print("\nJours extremes janvier :")
print(station_casa.jours_extremes("janvier"))

print("\nJours beaux janvier :")
print(station_casa.jours_beaux("janvier"))

print("\nScore moyen janvier :")
print(station_casa.score_moyen("janvier"))

print("\nMois le plus beau :")
print(station_casa.mois_beau())


# =========================================================
# QUESTION 6
# EXPORT CSV
# =========================================================
station_casa.exporter_csv()
station_rabat.exporter_csv()
station_fes.exporter_csv()
station_marrakech.exporter_csv()


# =========================================================
# SAUVEGARDE PICKLE
# =========================================================
stations = [
    station_casa,
    station_rabat,
    station_fes,
    station_marrakech
]

with open("stations.pkl", "wb") as f:
    pickle.dump(stations, f)

print("\nFichier stations.pkl créé avec succès !")


# =========================================================
# LECTURE DU PICKLE (TEST)
# =========================================================
with open("stations.pkl", "rb") as f:
    stations_chargees = pickle.load(f)

print("\n===== STATIONS CHARGEES =====")

for s in stations_chargees:
    print(s)