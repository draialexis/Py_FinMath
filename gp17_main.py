from math import log10

epsilon = 0.0001
t_min = 0.0
t_max = 1.0
nom_fichier = "gp17_data.txt"

decimals = -1 * int(log10(epsilon))  # La précision qu'on peut demander à l'affichage

#   1)

# La durée considérée pour le projet, en années
global DUREE
# L'investissement, en début de projet
global INIT_FLUX
# Les bénéfices réalisés en fin d'année
global BENEFICES
# Le prix de revente du matériel, en fin de projet
global REVENTE
REVENTE = 0




#   2)

# On suppose que les fichers xlsx suivent tous le même format
def lecture_donnees(in_donnees_xlsx):

    global DUREE
    global INIT_FLUX
    global BENEFICES
    global REVENTE


    try:  # si le fichier existe, on peut exploiter les données
        with open(in_donnees_xlsx) as f:
            for line_num, line in enumerate(f):

                if line_num == 0:
                    DUREE = int(line.strip())

                if line_num == 2:
                    data = line.strip().split(";")
                    INIT_FLUX = int(data.pop(0))  # on retire le premier element et on copie sa valeur dans init_flux
                    REVENTE = int(data.pop())  # on retire le dernier element et on copie sa valeur dans revente
                    BENEFICES = [int(i) for i in data]  # le reste de la liste sont les bénéfices de t=1 à t=n

    # si le fichier est introuvable, on utilise en dur les données correspondant au groupe 17 par défaut


    except FileNotFoundError:

        print("\n [WARNING] le fichier "
              + in_donnees_xlsx +
              " est introuvable, donc init_dicho() utilise en dur les donnees correspondant au groupe 17 par defaut.")

        DUREE = 7
        INIT_FLUX = -10400
        BENEFICES = [6100, 6400, 4300, 2000, 4900, 4400, 1500]
        REVENTE = 1040




#   3)

# On applique la formule du calcul de la VAN
def calcul_van(in_taux):

    if in_taux < 0:
        exit(" calcul_VAN(): taux < 0 INVALIDE ( in_taux =" + str(in_taux) + ")")

    van = INIT_FLUX

    for i, benefice in enumerate(BENEFICES):
        van = van + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    van = van + (REVENTE / pow(1 + in_taux, DUREE))

    return van




#   4)

# Procedure de validation des données du projet
def init_dicho(in_t_min, in_t_max):

    profits = 0.0

    for flux in BENEFICES:
        profits += flux
    profits += REVENTE

    # On vérifie que :
    # le projet est profitable en théorie
    # le flux initial est bien négatif
    # le taux minimum initial de dicho n'est pas négatif (VAN(t) est définie sur R+, pas sur tout R)
    # le taux minimum initial est bien strictement inférieur au taux maximum initial

    if profits + INIT_FLUX < 0 \
            or INIT_FLUX > 0 \
            or in_t_min < 0 \
            or in_t_max <= in_t_min:
        exit("init_dicho(): la question du TRI ne s'applique pas à ces données")




#   5)

# Suivi exact de la procédure à l'algo 5
# Diviser pour regner, convergence rapide vers l'objectif...
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


#   6)

def affichage_resultat(in_t_min, in_t_max, in_epsilon, in_t_ri):
    print("\n  Nombre de periodes (n) : " + str(DUREE))
    print("  Premier flux (I) : " + str(INIT_FLUX))
    print("  Benefices (B_i) : " + str(BENEFICES))
    print("  Valeur de revente de l'equipement (V) : " + str(REVENTE))
    print("\n [INFO] les bornes et l'epsilon peuvent etre modifies en dur, aux lignes 3, 4, et 5")

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("  Taux : borne inferieure = ( " + str(in_t_min) + " ) ; borne superieure = ( " + str(in_t_max) + " )")
    print("  Epsilon : " + str(in_epsilon))
    print("  Taux de rendement interne du projet : " + str(round(in_t_ri, decimals)))
    print("  Soit " + str(round((in_t_ri * 100), decimals - 2)) + "%")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# TEST

lecture_donnees(nom_fichier)
resultat = dichotomie(t_min, t_max, epsilon)
affichage_resultat(t_min, t_max, epsilon, resultat)
