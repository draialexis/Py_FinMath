import openpyxl

epsilon = 0.0001
t_min = 0.0
t_max = 1.0
nom_fichier = "gp17_data.xlsx"

# 1)

# la durée considérée pour le projet, en années
global DUREE
# l'investissement, en début de projet
global INIT_FLUX
# les bénéfices réalisés en fin d'année
global BENEFICES
# le prix de revente du matériel, en fin de projet
global REVENTE
REVENTE = 0


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

    try:  # si le fichier existe, on peut exploiter les données
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

        wb.close()

    # si le fichier est introuvable, on utilise en dur les données correspondant au groupe 17 par défaut
    except FileNotFoundError:
        print("\n[WARNING] le fichier "
              + in_donnees_xlsx +
              " est introuvable, donc init_dicho() utilise en dur les donnees correspondant au groupe 17 par defaut.")
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

    # on vérifie que :
    # le projet est profitable en théorie
    # le flux initial est bien négatif
    # le taux minimum initial de dicho n'est pas négatif (VAN(t) est définie sur R+, pas sur tout R)
    # le taux minimum initial est bien strictement inférieur au taux maximum initial
    if profits + INIT_FLUX < 0 \
            or INIT_FLUX > 0 \
            or in_t_min < 0 \
            or in_t_max <= in_t_min:
        exit("init_dicho(): la question du TRI ne s'applique pas à ces données")


# 5)

# suivi exact de la procédure à l'algo 5
# diviser pour regner, convergence rapide vers l'objectif...
def dichotomie(in_t_min, in_t_max, in_epsilon):
    init_dicho(in_t_min, in_t_max)  # validation grace à init_dicho

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

def affichage_resultat(in_t_min, in_t_max, in_epsilon, in_t_ri):
    print("\nnombre de periodes (n) : " + str(DUREE))
    print("premier flux (I) : " + str(INIT_FLUX))
    print("benefices (B_i) : " + str(BENEFICES))
    print("valeur de revente de l'equipement (V) : " + str(REVENTE))
    print("\n[INFO] les bornes et l'epsilon peuvent etre modifies en dur, aux lignes 3, 4, et 5")

    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("taux - borne inferieure : " + str(in_t_min) + " ; borne superieure : " + str(in_t_max))
    print("epsilon : " + str(in_epsilon))
    print("taux de rendement interne du projet : " + str(in_t_ri))
    print("soit " + str(round((in_t_ri * 100), 2)) + "%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


# TEST

lecture_donnees(nom_fichier)
resultat = dichotomie(t_min, t_max, epsilon)
affichage_resultat(t_min, t_max, epsilon, resultat)
