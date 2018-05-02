class Result:
    def __init__(self,blue,purple,blueResult,date):
        self.blue = blue
        self.purple = purple
        self.blueResult = blueResult
        self.date = date
        
        blue.newResult(self)
        purple.newResult(self)

    def clear(self):
        """
        retire le Result des Team.resultsList
        """
        self.blue.resultsList.remove(self)
        self.purple.resultsList.remove(self)
        
        
    def scoreOfTeam(self,team):
        """
        Retourne le score obtenue par le Team
        """
        if self.blueResult == 1 and self.blue == team:
            return 1
        if self.blueResult == 0 and self.purple == team:
            return 1
        return 0
    
    def getLoser(self):
        """
        Retourne le Team perdant
        """
        if self.blueResult == 1:
            return self.purple
        
        return self.blue
    
    def getOpponentOf(self,team):
        """
        Retourne le Team adversaire de Team
        """
        if self.blue == team:
            return self.purple
        
        return self.blue
    
    def getSideOf(self,team):
        """
        Retourne la couleur de Team
        """
        if self.blue == team:
            return "blue"
        
        return "purple"