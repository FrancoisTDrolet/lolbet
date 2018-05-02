import datetime

class Team:
    def newResult(self,result):
        """
        ajoute un objet Result a la self.resultsList
        """
        self.resultsList.append(result)
        if result.date>self.lastDateActive:
            self.lastDateActive = result.date
        
    def __init__(self,name,elo = 0):
        self.name = name
        self.elo = elo
        self.resultsList = []
        self.lastDateActive = datetime.date(1,1,1)
        
    def getTeamsBeatenSet(self):
        """
        Renvoie le set des Team contre lesquel self a une victoire 
        """
        teamsBeatenSet = set()
        
        for result in self.resultsList:
            if result.scoreOfTeam(self) == 1:
                teamsBeatenSet.add(result.getLoser())
                
        return teamsBeatenSet
        
    def isConnectedByWinsTo(self,team):
        """
        test si self est relier a Team par une chaine de victoires
        """
        teamsToVisitSet = set()
        teamVisitedSet = set()
        teamsToVisitSet.add(self)
        
        while not(teamsToVisitSet == set()):
            currentTeam = teamsToVisitSet.pop()
            
            if currentTeam == team:
                return True
            
            teamVisitedSet.add(currentTeam)
            teamsToVisitSet.update(currentTeam.getTeamsBeatenSet())
            teamsToVisitSet.difference_update(teamVisitedSet)
            
        return False
    
    def isConnectedTo(self,team):
        """
        regarde si self est relier a Team par une chaine de victoires et de 
        defaites.
        """
        return (self.isConnectedByWinsTo(team) and team.isConnectedByWinsTo(self))
            
    def gradient(self,blueAdvantage,eloDecayHalfLife):
        """
        Retourne la derive partiel par raport a self.elo
        """
        gradient = 0
        
        for result in self.resultsList:
            opponentElo = result.getOpponentOf(self).elo
            selfElo = self.elo
            
            if result.getSideOf(self) == "blue":
                selfElo += blueAdvantage
            else:
                opponentElo += blueAdvantage
            
            if result.getLoser() == self:
                partial = -(10.0**((selfElo-opponentElo)/400.0)/(1+10**((selfElo-opponentElo)/400.0)))
                
            else:
                partial = 10.0**((opponentElo-selfElo)/400.0)/(1+10**((opponentElo-selfElo)/400.0)) 
                
            partial *= 2**(-(self.lastDateActive-result.date).total_seconds()/(2629800*eloDecayHalfLife))
            gradient += partial
        return gradient
    
    def getText(self,eloInt = 0):
        outStr = ""
        outStr += str(len(self.resultsList))
        outStr += ";"
        outStr += self.name
        outStr += ";"
        if eloInt == 1:
            outStr += str(int(round(self.elo)))
        else:
            outStr += str(self.elo)
        outStr += ";"
        
        return outStr