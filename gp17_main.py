from math import log10

EPSILON = 0.00001
T_MIN = 0.0
T_MAX = 1.0
NOM_FICHIER = "gp17_data.txt"

DECIMALS = -1 * int(log10(EPSILON))  # La précision qu'on peut demander à l'affichage

#   1)

# La durée considérée pour le projet, en années
global duree
# L'investissement, en début de projet
global init_flux
# Le prix de revente du matériel, en fin de projet
global revente
revente = 0
# Les bénéfices réalisés en fin d'année
global benefices




#   2)

# On suppose que les fichers de donnees suivent tous le même format
def lecture_donnees(in_donnees):

    global duree
    global init_flux
    global benefices
    global revente


    try:  # si le fichier existe, on peut exploiter les données
        with open(in_donnees) as f:
            for line_num, line in enumerate(f):

                if line_num == 0:
                    duree = int(line.strip())

                if line_num == 2:
                    data = line.strip().split(";")
                    init_flux = int(data.pop(0))  # on retire le premier element et on copie sa valeur dans init_flux
                    revente = int(data.pop())  # on retire le dernier element et on copie sa valeur dans revente
                    benefices = [int(i) for i in data]  # le reste de la liste sont les bénéfices de t=1 à t=n

    # si le fichier est introuvable, on utilise en dur les données correspondant au groupe 17 par défaut


    except FileNotFoundError:

        print("\n [WARNING] le fichier "
              + in_donnees +
              " est introuvable, donc init_dicho() utilise en dur les donnees correspondant au groupe 17 par defaut.")

        duree = 7
        init_flux = -10400
        benefices = [6100, 6400, 4300, 2000, 4900, 4400, 1500]
        revente = 1040




#   3)

# On applique la formule du calcul de la VAN
def calcul_van(in_taux):

    if in_taux < 0:
        exit(" calcul_VAN(): taux < 0 INVALIDE ( in_taux =" + str(in_taux) + ")")

    van = init_flux

    for i, benefice in enumerate(benefices):
        van = van + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    van = van + (revente / pow(1 + in_taux, duree))

    return van




#   4)

# Procedure de validation des données du projet
def init_dicho(in_t_min, in_t_max):

    profits = 0.0

    for flux in benefices:
        profits += flux
    profits += revente

    # On vérifie que :
    # le projet est profitable en théorie
    # le flux initial est bien négatif
    # le taux minimum initial de dicho n'est pas négatif (VAN(t) est définie sur R+, pas sur tout R)
    # le taux minimum initial est bien strictement inférieur au taux maximum initial

    if profits + init_flux < 0 \
            or init_flux > 0 \
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
    print("\n  Nombre de periodes (n) : " + str(duree))
    print("  Premier flux (I) : " + str(init_flux))
    print("  Benefices (B_i) : " + str(benefices))
    print("  Valeur de revente de l'equipement (V) : " + str(revente))
    print("\n [INFO] les bornes et l'epsilon peuvent etre modifies en dur, aux lignes 3, 4, et 5")

    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("  Taux : borne inferieure = ( " + str(in_t_min) + " ) ; borne superieure = ( " + str(in_t_max) + " )")
    print("  Epsilon : " + str(in_epsilon))
    print("  Taux de rendement interne du projet : " + str(round(in_t_ri, DECIMALS)))
    print("  Soit " + str(round((in_t_ri * 100), DECIMALS - 2)) + "%")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

# TEST

lecture_donnees(NOM_FICHIER)
resultat = dichotomie(T_MIN, T_MAX, EPSILON)
affichage_resultat(T_MIN, T_MAX, EPSILON, resultat)
