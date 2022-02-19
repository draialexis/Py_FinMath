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
    print("Looks like we're gonna need pandas")
    # https://www.sitepoint.com/using-python-parse-spreadsheet-data/
    # TODO implement function for real


# 3)

def calcul_van(in_taux):
    if in_taux < 0:
        exit("calcul_VAN(): some error message")

    van = investissement
    for i, benefice in enumerate(benefices):
        van = van + (benefice / pow(1 + in_taux, i + 1))  # attention, i est 0-indexé...

    van = van + (revente / pow(1 + in_taux, duree))
    return van


# 4)

def init_dicho(in_epsilon):
    print("not today!")

    in_t_max = in_t_min = 0.0
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
        else:
            if van_c <= - in_epsilon:
                in_t_min = t_c
            else:
                t_ri = t_c
                arret = True

    return t_ri


# 6)

def affichage_resultat(t_ri):
    print("we'll figure something out..." + t_ri)
    # TODO implement function for real
