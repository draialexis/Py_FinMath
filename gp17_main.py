from os import path

import openpyxl

# 1)
# la durée considérée pour le projet, en années
global DUREE
# l'investissement, en début de projet
global INIT_FLUX
# les bénéfices réalisés en fin d'année
global BENEFICES
# le prix de revente du matériel, en fin de projet
global REVENTE


# 2)

# fonction annexe pour incrémenter le premier charactere d'un string de 1 char (B4 -> C4, etc.)
def increment_char(char):
    b = bytes(char, 'utf-8')
    b = b[0] + 1
    return chr(b)


# on suppose que les fichers xlsx suivent tous le même format
def lecture_donnees(in_donnees_xlsx):
    global DUREE
    global INIT_FLUX
    global BENEFICES
    global REVENTE

    if path.exists(in_donnees_xlsx):
        wb = openpyxl.load_workbook(in_donnees_xlsx)
        sheet = wb.active

        DUREE = sheet["B2"].value

        INIT_FLUX = sheet["B4"].value

        BENEFICES = []
        char = "B"
        for i in range(DUREE):
            char = increment_char(char)
            BENEFICES.append(sheet[char + "4"].value)

        char = increment_char(char)

        REVENTE = sheet[char + "4"].value

    else:  # si le fichier est introuvable, on utilise des données hardcoded correspondant au groupe 17
        DUREE = 7
        INIT_FLUX = -10400
        BENEFICES = [6100, 6400, 4300, 2000, 4900, 4400, 1500]
        REVENTE = 1040


# 3)

# on applique la formule du calcul de la VAN
def calcul_van(in_taux):
    if in_taux < 0:
        exit("calcul_VAN(): taux < 0 INVALIDE ( in_taux =" + str(in_taux) + ")")

    van = INIT_FLUX
    for i, benefice in enumerate(BENEFICES):
        van = van + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    van = van + (REVENTE / pow(1 + in_taux, DUREE))
    return van


# 4)

# procedure de validation des données du projet
def init_dicho(in_t_min, in_t_max):
    profits = 0.0

    for flow in BENEFICES:
        profits += flow

    # le projet est profitable en theorie
    # le flux initial est bien négatif
    # le taux minimum initial de dicho n'est pas négatif (VAN(t) est définie sur R+, pas R)
    if profits + INIT_FLUX < 0 \
            or INIT_FLUX > 0 \
            or in_t_min < 0 \
            or in_t_max <= in_t_min:
        exit("dichotomie(): la question du TRI ne s'applique pas à ces données")

    return True


# 5)

# suivi exact de la procédure à l'algo 5
# diviser pour regner, convergence rapide vers l'objectif...
def dichotomie(in_t_min, in_t_max, in_epsilon):
    init_dicho(in_t_min, in_t_max)
    # validation grace à init_dicho
    t_ri = 0.0
    arret = False
    while not arret:
        t_c = (in_t_max + in_t_min) / 2
        van_c = calcul_van(t_c)
        if van_c >= in_epsilon:
            in_t_min = t_c
        elif van_c <= - in_epsilon:
            in_t_max = t_c
        else:
            t_ri = t_c
            arret = True

    return t_ri


# 6)

def affichage_resultat(t_ri):
    print("\nnombre de periodes (n) : " + str(DUREE))
    print("premier flux (I) : " + str(INIT_FLUX))
    print("benefices (B_i) : " + str(BENEFICES))
    print("valeur de revente de l'equipement (V) : " + str(REVENTE))

    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("taux de rendement interne du projet (t_ri) : " + str(t_ri))
    print("soit " + str(round((t_ri * 100), 2)) + "%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


# TEST

lecture_donnees('gp17_data.xlsx')
affichage_resultat(dichotomie(0, 1, 0.0001))  # epsilon = 0.0001, suggéré
