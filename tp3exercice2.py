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

        # TEMPERATURE
        if 18 <= t <= 28:
            s += 25
        elif 10 <= t < 18 or 28 < t <= 32:
            s += 15
        else:
            s += 5

        # HUMIDITE
        if 40 <= h <= 70:
            s += 15
        elif 30 <= h < 40 or 70 < h <= 80:
            s += 8
        else:
            s += 3

        # PRECIPITATIONS
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

annee = [
    ("janvier",   31),
    ("fevrier",   29),
    ("mars",      31),
    ("avril",     30),
    ("mai",       31),
    ("juin",      30),
    ("juillet",   31),
    ("aout",      31),
    ("septembre", 30),
    ("octobre",   31),
    ("novembre",  30),
    ("decembre",  31)
]


# =========================================================
# NOUVEAU (Q1) : MOYENNES MENSUELLES REALISTES
# Chaque tuple : (temperature, humidite, precipitations,
#                 vent, pression, indice_uv)
# =========================================================
moyennes = {
    "janvier":   (12, 75, 5,   18, 1018, 2),
    "fevrier":   (13, 72, 4,   18, 1017, 3),
    "mars":      (16, 68, 3,   17, 1016, 4),
    "avril":     (18, 63, 3,   16, 1015, 5),
    "mai":       (22, 58, 2,   15, 1014, 7),
    "juin":      (26, 52, 1,   14, 1013, 9),
    "juillet":   (30, 45, 0.5, 13, 1012, 10),
    "aout":      (31, 47, 0.5, 13, 1012, 10),
    "septembre": (27, 55, 2,   14, 1014, 8),
    "octobre":   (22, 63, 3,   15, 1015, 5),
    "novembre":  (17, 70, 4,   17, 1017, 3),
    "decembre":  (13, 76, 5,   18, 1018, 2)
}


# =========================================================
# CLASSE STATION
# MODIFIEE pour l'exercice 2 :
#   - generer_donnees() utilise np.random.normal()
#   - self.__data a maintenant 3 niveaux : annee > mois > jour
#   - exporter_csv() ajoute la colonne annee
#   - toutes les methodes prennent annee en parametre
# =========================================================
class Station:

    def __init__(self, nom, localisation):
        self.__nom = nom
        self.__localisation = localisation

        # NOUVEAU : data[annee][mois][jour] = Enregistrement
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
    # NOUVEAU (Ex2 Q1) : GENERATION REALISTE AVEC np.random.normal
    # =========================================================
    def generer_donnees(self):

        # On genere les donnees pour 3 annees
        for annee_num in [2023, 2024, 2025]:

            self.__data[annee_num] = {}

            for mois, nb_jours in annee:

                self.__data[annee_num][mois] = {}

                # On recupere les moyennes du mois depuis le dictionnaire
                moy_t, moy_h, moy_p, moy_v, moy_pr, moy_uv = moyennes[mois]

                for jour in range(1, nb_jours + 1):

                    # -- temperature : centree sur moy_t, ecart-type 3, bornee [-5, 45]
                    temperature = np.clip(np.random.normal(moy_t, 3), -5, 45)
                    temperature = round(float(temperature), 1)
                    # 1 chance sur 8 d'avoir une valeur manquante
                    if random.randint(1, 8) == 1:
                        temperature = np.nan

                    # -- humidite : centree sur moy_h, ecart-type 5, bornee [0, 100]
                    humidite = np.clip(np.random.normal(moy_h, 5), 0, 100)
                    humidite = round(float(humidite), 1)
                    if random.randint(1, 8) == 1:
                        humidite = np.nan

                    # -- precipitations : centrees sur moy_p, ecart-type 2, bornees [0, 50]
                    precipitations = np.clip(np.random.normal(moy_p, 2), 0, 50)
                    precipitations = round(float(precipitations), 1)
                    if random.randint(1, 8) == 1:
                        precipitations = np.nan

                    # -- vent : centre sur moy_v, ecart-type 4, borne [0, 120]
                    vent = np.clip(np.random.normal(moy_v, 4), 0, 120)
                    vent = round(float(vent), 1)
                    if random.randint(1, 8) == 1:
                        vent = np.nan

                    # -- pression : centree sur moy_pr, ecart-type 3, bornee [970, 1050]
                    pression = np.clip(np.random.normal(moy_pr, 3), 970, 1050)
                    pression = round(float(pression), 1)
                    if random.randint(1, 8) == 1:
                        pression = np.nan

                    # -- indice UV : centre sur moy_uv, ecart-type 1, borne [0, 11]
                    indice_uv = np.clip(np.random.normal(moy_uv, 1), 0, 11)
                    indice_uv = round(float(indice_uv), 1)
                    if random.randint(1, 8) == 1:
                        indice_uv = np.nan

                    enregistrement = Enregistrement(
                        temperature,
                        humidite,
                        precipitations,
                        vent,
                        pression,
                        indice_uv
                    )

                    self.__data[annee_num][mois][jour] = enregistrement

    # =========================================================
    # LISTE DES ENREGISTREMENTS
    # On passe maintenant annee en parametre
    # =========================================================
    def _liste_enregistrements(self, annee_num, mois):
        return list(self.__data[annee_num][mois].values())

    # =========================================================
    # TEMPERATURES UNIQUES
    # =========================================================
    def temperatures_uniques(self, annee_num, mois):

        liste = []

        for e in self._liste_enregistrements(annee_num, mois):

            t = e.getTemperature()

            if not np.isnan(t):
                liste.append(t)

        return list(set(liste))

    # =========================================================
    # TEMPERATURE MOYENNE
    # =========================================================
    def temperature_moyenne(self, annee_num, mois):

        liste = []

        for e in self._liste_enregistrements(annee_num, mois):

            t = e.getTemperature()

            if not np.isnan(t):
                liste.append(t)

        if len(liste) > 0:
            return round(sum(liste) / len(liste), 2)

        return np.nan

    # =========================================================
    # JOURS PLUVIEUX
    # =========================================================
    def jours_pluvieux(self, annee_num, mois):

        jours = []

        for jour, e in self.__data[annee_num][mois].items():

            p = e.getPrecipitations()

            if not np.isnan(p) and p > 0:
                jours.append(jour)

        return jours

    # =========================================================
    # JOURS EXTREMES
    # =========================================================
    def jours_extremes(self, annee_num, mois):

        jours = []

        for jour, e in self.__data[annee_num][mois].items():

            t = e.getTemperature()

            if not np.isnan(t) and (t < 5 or t > 35):
                jours.append(jour)

        return jours

    # =========================================================
    # HUMIDITE MOYENNE
    # =========================================================
    def humidite_moyenne(self, annee_num, mois):

        liste = []

        for e in self._liste_enregistrements(annee_num, mois):

            h = e.getHumidite()

            if not np.isnan(h):
                liste.append(h)

        if len(liste) > 0:
            return round(sum(liste) / len(liste), 2)

        return np.nan

    # =========================================================
    # PRECIPITATIONS TOTALES
    # =========================================================
    def precipitations_totales(self, annee_num, mois):

        total = 0

        for e in self._liste_enregistrements(annee_num, mois):

            p = e.getPrecipitations()

            if not np.isnan(p):
                total += p

        return round(total, 2)

    # =========================================================
    # JOURS BEAUX
    # =========================================================
    def jours_beaux(self, annee_num, mois):

        jours = []

        for jour, e in self.__data[annee_num][mois].items():

            if e.score() >= 80:
                jours.append(jour)

        return jours

    # =========================================================
    # SCORE MOYEN
    # =========================================================
    def score_moyen(self, annee_num, mois):

        scores = []

        for e in self._liste_enregistrements(annee_num, mois):
            scores.append(e.score())

        if len(scores) > 0:
            return round(sum(scores) / len(scores), 2)

        return 0

    # =========================================================
    # MOIS LE PLUS BEAU
    # =========================================================
    def mois_beau(self, annee_num):

        meilleur_mois = None
        meilleur_score = -1

        for mois, _ in annee:

            s = self.score_moyen(annee_num, mois)

            if s > meilleur_score:
                meilleur_score = s
                meilleur_mois = mois

        return meilleur_mois

    # =========================================================
    # NOUVEAU (Q2) : EXPORT CSV AVEC COLONNE ANNEE
    # Structure : annee, mois, jour, temperature, humidite,
    #             precipitations, vent, pression, indice_uv, score
    # =========================================================
    def exporter_csv(self):

        # On ajoute _v2 pour ne pas ecraser les fichiers de l'exercice 1
        nom_fichier = self.__nom + "_v2.csv"

        with open(nom_fichier, "w", newline="", encoding="utf-8") as f:

            writer = csv.writer(f)

            # En-tete : on ajoute la colonne annee au debut
            writer.writerow([
                "annee",
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

            # On parcourt les annees dans l'ordre
            for annee_num in sorted(self.__data.keys()):

                for mois, _ in annee:

                    for jour, e in self.__data[annee_num][mois].items():

                        writer.writerow([
                            annee_num,
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

        print("CSV cree :", nom_fichier)
    def __str__(self):
        return (
            "Station : " + self.__nom +
            " | Localisation : " + self.__localisation
        )


# =========================================================
# CREATION DES STATIONS
# =========================================================
station_casa = Station("Station_Casa", "Casablanca")
station_rabat = Station("Station_Rabat", "Rabat")
station_fes = Station("Station_Fes", "Fes")
station_marrakech = Station("Station_Marrakech", "Marrakech")


# =========================================================
# TESTS DES METHODES
# On teste avec annee=2024, mois="janvier"
# =========================================================
print("\n===== TESTS =====\n")

print(station_casa)

print("\nTemperature moyenne janvier 2024 :")
print(station_casa.temperature_moyenne(2024, "janvier"))

print("\nHumidite moyenne janvier 2024 :")
print(station_casa.humidite_moyenne(2024, "janvier"))

print("\nPrecipitations totales janvier 2024 :")
print(station_casa.precipitations_totales(2024, "janvier"))

print("\nJours pluvieux janvier 2024 :")
print(station_casa.jours_pluvieux(2024, "janvier"))

print("\nJours extremes janvier 2024 :")
print(station_casa.jours_extremes(2024, "janvier"))

print("\nJours beaux janvier 2024 :")
print(station_casa.jours_beaux(2024, "janvier"))

print("\nScore moyen janvier 2024 :")
print(station_casa.score_moyen(2024, "janvier"))

print("\nMois le plus beau 2024 :")
print(station_casa.mois_beau(2024))


# =========================================================
# EXPORT CSV - un fichier par station avec les 3 annees
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

with open("stations_v2.pkl", "wb") as f:
    pickle.dump(stations, f)

print("\nFichier stations_v2.pkl cree avec succes !")


# =========================================================
# LECTURE DU PICKLE (TEST)
# =========================================================
with open("stations_v2.pkl", "rb") as f:
    stations_chargees = pickle.load(f)

print("\n===== STATIONS CHARGEES =====")

for s in stations_chargees:
    print(s)