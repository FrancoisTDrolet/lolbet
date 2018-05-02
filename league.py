import datetime
from result import *
from lolbetTools import *
from team import *
import sys

ELO_DECAY_HALFLIFE = 2.5
GRADIENT_DESCENT_STEP = 20

class League:
    def __init__(self):
        self.teamsDictionary = {}
        self.blueAdvantage = 0
        self.resultsList = []
        self.eloDecayHalfLife = ELO_DECAY_HALFLIFE
        self.gradientDescentStep = GRADIENT_DESCENT_STEP

    def newResult(self,blueTeam,purpleTeam,blueResult,date):
        
        if type(blueTeam) is str:
            blueTeamName = blueTeam
            
            if not(self.teamsDictionary.has_key(blueTeam)):
                blueTeam = Team(blueTeamName)
                self.teamsDictionary[blueTeamName] = blueTeam
            else:
                blueTeam = self.teamsDictionary[blueTeamName]
        
        if type(purpleTeam) is str:
            purpleTeamName = purpleTeam
            if not(self.teamsDictionary.has_key(purpleTeam)):
                purpleTeam = Team(purpleTeamName)
                self.teamsDictionary[purpleTeamName] = purpleTeam
            else:
                purpleTeam = self.teamsDictionary[purpleTeamName]
                
        
        self.resultsList.append(Result(blueTeam,purpleTeam,blueResult,date))
                                

    def getAverageElo(self):
        avgElo = 0
        for team in self.teamsDictionary.values():
            avgElo += team.elo
            
        return avgElo/len(self.teamsDictionary.values())
        
    def normalize(self):
        avgElo = self.getAverageElo()
        for team in self.teamsDictionary.values():
            team.elo -=avgElo
            
        
        
    def teamsFromFile(self,fileName):
        dataFile = open(fileName,"r")
        for line in dataFile.readlines():
            data = line.split(";")
            if data[0] == "blue advantage":
                self.blueAdvantage = float(data[1])
                continue
            if data[1] == "name":
                continue
            self.teamsDictionary[data[1]] = Team(data[1],float(data[2]))
            
        dataFile.close()
        
    def teamsToFile(self,fileName):
        dataFile = open(fileName,"w")
        dataFile.write("blue advantage;" + str(self.blueAdvantage) + ";\n")
        dataFile.write("n Data;name;elo;\n")
        for team in self.teamsDictionary.values():
            dataFile.write(team.getText()+";\n")
        dataFile.close()
            
        

    def purge(self):
        """
        Retire les parties entres joueurs non-conectes de self.resultsList de
        League et des Team implique 
        """
        for result in self.resultsList:
            if not(result.blue.isConnectedTo(result.purple)):
                result.clear()
                
    def getTeam(self,teamName):
        """
        Prend un str et retourne le Team
        """
        return self.teamsDictionary[teamName]
        
    def buildFromFile(self,fileName):
        """
        Ajoute a League les resultats et equipe du fichier fileName
        """
        
        file = open(fileName,"r")
        
        for line in file.readlines():
            data = line.split(";")
            
            if data[0] == "Team 1":
                continue
            
            if data[9]=="0":
                continue
            
            if not(self.teamsDictionary.has_key(data[0])):
                self.teamsDictionary[data[0]] = Team(data[0])
                
            if not(self.teamsDictionary.has_key(data[1])):
                self.teamsDictionary[data[1]] = Team(data[1])
                
            dateData = data[4].split("/")
        
            if dateData == ['date']:
                continue
        
            y = int(dateData[2])
            m = int(dateData[1])
            d = int(dateData[0])  
            
             
            if int(data[3]) == 1:
                blueTeam = self.teamsDictionary[data[0]]
                purpleTeam = self.teamsDictionary[data[1]]
            else:
                blueTeam = self.teamsDictionary[data[1]]
                purpleTeam = self.teamsDictionary[data[0]]
                
            purpleTeamWins = (int(data[2])+int(data[3]))%2
            
            self.resultsList.append(Result(blueTeam,purpleTeam,1-purpleTeamWins,datetime.date(y,m,d)))
            
        file.close()
        
    def gradientNorm(self):
        """
        Retourne la norme du gradient.
        """
        gradientNorm = abs(self.blueAdvantageGradient())
        
        for team in self.teamsDictionary.values():
            gradientNorm += abs(team.gradient(self.blueAdvantage,self.eloDecayHalfLife))
        return gradientNorm
    
    def gradientDescent(self,stop = 0.0,display = 1):
        """
        Optimise les Team.elo et self.blueAdvantage.
        """
        if display == 1:
            while self.gradientNorm() > stop:
                for team in self.teamsDictionary.values():
                    team.elo += team.gradient(self.blueAdvantage,self.eloDecayHalfLife)*self.gradientDescentStep
                self.blueAdvantage += self.blueAdvantageGradient()*self.gradientDescentStep/100.0
                sys.stdout.write("\r"+str(self.gradientNorm()))
                sys.stdout.flush()
        else:
            while self.gradientNorm() > stop:
                for team in self.teamsDictionary.values():
                    team.elo += team.gradient(self.blueAdvantage,self.eloDecayHalfLife)*self.gradientDescentStep
                self.blueAdvantage += self.blueAdvantageGradient()*self.gradientDescentStep/100.0
                
    def bulletin(self):
        """
        Print la liste des Team.name avec leurs Team.elo du self.teamsDictionary.
        """
        print "blue advantage = " + str(self.blueAdvantage)
        sorted = sortTeamListByElo(self.teamsDictionary.values())
        for team in sorted:
            print team.getText(1)
                
    def blueAdvantageGradient(self):
        """
        Retourn la derive partiel pour self.blueAdvantage
        """
        today = datetime.date.today()
        gradient = 0
        
        for result in self.resultsList:
            opponentElo = result.purple.elo-result.blue.elo
            selfElo = self.blueAdvantage
            
            if result.getLoser() == result.blue:
                partial = -(10.0**((selfElo-opponentElo)/400.0)/(1+10**((selfElo-opponentElo)/400.0)))
                
            else:
                partial = 10.0**((opponentElo-selfElo)/400.0)/(1+10**((opponentElo-selfElo)/400.0)) 
                
            partial *= 2**(-(today-result.date).total_seconds()/(2629800*self.eloDecayHalfLife))
            gradient += partial
        
        return gradient
     
    def probabilityOfResult(self,blueTeam,purpleTeam,blueScore,purpleScore,bestOf):
        """
        probabilityOfResult(Team,Team,int,int,int) = float. Retourne la 
        probabilite de se retrouver avec les score donnes dans un match demandant
        bestOf wins pour gagner
        """
        side = (blueScore+purpleScore)%2
        p = 0
        blueElo = blueTeam.elo + side*self.blueAdvantage
        purpleElo = purpleTeam.elo + (1-side)*self.blueAdvantage
        
        expectedScore = winProbabilityFromDeltaElo(blueElo-purpleElo)
        if (blueScore>0 and not(purpleScore >= bestOf)):
            p+=self.probabilityOfResult(blueTeam,purpleTeam,blueScore-1,purpleScore,bestOf)*expectedScore
        if (purpleScore>0 and not(blueScore >= bestOf)):
            p+=self.probabilityOfResult(blueTeam,purpleTeam,blueScore,purpleScore-1,bestOf)*(1-expectedScore)
        if (purpleScore ==0 and blueScore == 0):
            p = 1
            
        return p
                  
    def probabilityOfWinning(self,blueTeam,purpleTeam,bestOf,handicap):
        """
        probabilityOfWinning(Team,Team,int,float) = float. Retourne la
        probabilite pour blueTeam d'etre le pemier a avoir bestOf wins.
        """
        p = 0
        if handicap>=0:
            scorePurple = 0
            while scorePurple<(bestOf-handicap):
                p += self.probabilityOfResult(blueTeam,purpleTeam,bestOf,min(scorePurple,bestOf),bestOf)
                scorePurple += 1
        else:
            scoreBlue = 0 
            while scoreBlue<(bestOf+handicap):
                p += self.probabilityOfResult(blueTeam,purpleTeam,min(scoreBlue,bestOf),bestOf,bestOf)
                scoreBlue += 1
            p = 1-p
        return p