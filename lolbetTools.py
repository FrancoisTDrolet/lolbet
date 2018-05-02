import math

def nCr(n,r):
    """
    n choose r
    """
    f = math.factorial
    return f(n) / f(r) / f(n-r)
    
def winProbabilityFromDeltaElo(deltaElo):
    """
    donne la probabilite de victoire en fonction de l ecart des elos
    """
    return 1.0/(1.0+10.0**(-deltaElo/400.0))
    
def sortTeamListByElo(teamList):
    """
    Prend une liste de Team et en retourne un copie trier
    """
    toSort = teamList[:]
    sorted = []
    while not(toSort == []):
        maxElo = -1000
        for team in toSort:
            if team.elo>maxElo:
                newTeam = team
                maxElo = team.elo
        toSort.remove(newTeam)
        sorted.append(newTeam)
    return sorted