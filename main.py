import openpyxl

# 1)
# la durée considérée pour le projet, en années
global DUREE
# l'investissement, en début de projet
global INVESTISSEMENT
# les bénéfices réalisés en fin d'année
global BENEFICES
# le prix de revente du matériel, en fin de projet
global REVENTE


# 2)

def increment_char(char):
    b = bytes(char, 'utf-8')
    b = b[0] + 1
    return chr(b)


def lecture_donnees(in_donnees_xlsx):
    wb = openpyxl.load_workbook(in_donnees_xlsx)
    sheet = wb.active

    global DUREE
    DUREE = sheet["B2"].value

    global INVESTISSEMENT
    INVESTISSEMENT = sheet["B4"].value

    global BENEFICES
    BENEFICES = []
    char = "B"
    for i in range(DUREE):
        char = increment_char(char)
        BENEFICES.append(sheet[char + "4"].value)

    char = increment_char(char)
    global REVENTE
    REVENTE = sheet[char + "4"].value


# 3)

def calcul_van(in_taux):
    if in_taux < 0:
        exit("calcul_VAN(): some error message")

    van = INVESTISSEMENT
    for i, benefice in enumerate(BENEFICES):
        van = van + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    van = van + (REVENTE / pow(1 + in_taux, DUREE))
    return van


# 4)

def init_dicho(in_epsilon):
    # oooh this is a validation function

    in_t_max = in_t_min = 0.0  # initialized with nonsense values
    if in_epsilon >= 1.0:
        exit("init_dicho(): some error message")

    # TODO implement function for real
    return in_t_max, in_t_min


# 5)

def dichotomie(in_t_max, in_t_min, in_epsilon):
    # all conditions will be verified by init_dicho
    t_ri = 0.0
    arret = False
    while not arret:
        t_c = (in_t_max + in_t_min) / 2
        van_c = calcul_van(t_c)
        if van_c >= in_epsilon:
            in_t_max = t_c
        elif van_c <= - in_epsilon:
            in_t_min = t_c
        else:
            t_ri = t_c
            arret = True

    return t_ri


# 6)

def affichage_resultat(t_ri):

    print("\nnombre de periodes (n) : " + str(DUREE))
    print("premier flux (I) : " + str(INVESTISSEMENT))
    print("benefices (B_i) : " + str(BENEFICES))
    print("valeur de revente de l'equipement (V) : " + str(REVENTE))

    print("\n%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("taux de rendement interne du projet (t_ri) : " + str(t_ri))
    print("soit " + str(round((t_ri * 100), 2)) + "%")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")


lecture_donnees('gp17_data.xlsx')
res = dichotomie(0, 1, 0.0001)
affichage_resultat(res)
"""
epsilon = 0.0001, suggéré

Le rapport, au format pdf, contiendra la partie théorique, la description algorithmique des procédures
programmées et le résultat obtenu sur les données.
"""
