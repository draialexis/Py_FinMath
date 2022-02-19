# 1)
# la durée considérée pour le projet, en années
global duree
# l'investissement, en début de projet
global investissement
# le prix de revente du matériel, en fin de projet
global revente
# les bénéfices réalisés en fin d'année
global benefices


# 2)

def lecture_donnees():
    print("I don't want to :'(")


# 3)

def calcul_VAN(in_taux):
    if in_taux < 0:
        exit("calcul_VAN(): some error message")

    VAN = investissement
    for i, benefice in enumerate(benefices):
        VAN = VAN + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    VAN = VAN + (revente / pow(1 + in_taux, duree))
    return VAN


# 4)

def init_dicho(in_epsilon):
    t_m = t_M = 0.0
    print("not today!")
    return t_m, t_M


# 5)

def dichotomie(in_t_m, in_t_M, in_epsilon):
    # all conditions will be verified by init_dicho
    t_ri = t_c = VAN_c = 0.0
    arret = False
    while not arret:
        t_c = (in_t_m + in_t_M) / 2
        VAN_c = calcul_VAN(t_c)
        if VAN_c >= in_epsilon:
            in_t_m = t_c
        else:
            if VAN_c <= -in_epsilon:
                in_t_M = t_c
            else:
                t_ri = t_c
                arret = True

    return t_ri


# 6)

def affichage_resultat(t_ri):
    print("we'll figure something out...")
