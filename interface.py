from lolbet import *
import os

TH_WEIGHT = 1.0

def moneyLine(blueTeam,purpleTeam,bestOf=1,handicap=0):
    if isinstance(blueTeam,str):
        blueTeam = league.teamsDictionary[blueTeam]
        
    if isinstance(purpleTeam,str):
        purpleTeam = league.teamsDictionary[purpleTeam]
    
    if not(blueTeam.isConnectedTo(purpleTeam)):
        print "warning teams not connected"    
    p = league.probabilityOfWinning(blueTeam,purpleTeam,bestOf,handicap)
    
    return 1/p, 1/(1-p)

def theirMoneyLine(m,M):
    p = ((1.0/m + (1.0-1.0/M))/2.0)
    return 1.0/p , 1.0/(1-p)
    
def kelly(myMoneyLine,theMoneyLine):
    M = theMoneyLine
    w = 1.0/myMoneyLine
    return (w*M-1)/(M-1)
    
def bet(blueTeamName,purpleTeamName,blueMoneyLine,purpleMoneyLine,bestOf=1,handicap = 0):
    myBlueLine,myPurpleLine = moneyLine(blueTeamName,purpleTeamName,bestOf,handicap)
    thBlueLine,thPurpleLine = theirMoneyLine(blueMoneyLine,purpleMoneyLine)
    avgBlueLine = (myBlueLine*(1.0-TH_WEIGHT)+thBlueLine*TH_WEIGHT)/2.0
    avgPurpleLine = (myPurpleLine*(1.0-TH_WEIGHT) + thPurpleLine*TH_WEIGHT)/2.0
    if avgBlueLine < blueMoneyLine:
        return blueTeamName,myBlueLine,kelly(avgBlueLine,blueMoneyLine)
    if avgPurpleLine < purpleMoneyLine:
        return purpleTeamName,myPurpleLine,kelly(avgPurpleLine,purpleMoneyLine)
    return "Dont!"

def allBet(bankroll):
    file = open("betsData.csv","r")
    betData = []
    for lineR in file.readlines():
        line = lineR.split(";")
        if line[0] == "blue":
            continue
        newData = [line[0],line[1],float(line[2]),float(line[3]),int(line[4]),int(line[5]),int(line[6]),float(line[7])]
        dateData = line[8].split("/")
        newDate = datetime.date(int(dateData[2]),int(dateData[1]),int(dateData[0]))
        newData.append(newDate)
        betData.append(newData)
    
    bets = []
    for bett in betData:
        forOut = list(bet(bett[0],bett[1],bett[2],bett[3],bett[4],bett[5]))
        forOut.append(bett[6])
        forOut.append(bett[7])
        bets.append(forOut)
        if bets[-1][0] == "D":
            bets.pop()
    
    totalToBet = 1
    sum = 0
    
    for bett in bets:
        totalToBet *= 1.0 - bett[2]
        sum += bett[2]
        
    totalToBet = 1-totalToBet
    
    for bett in bets:
        bett[2] = bett[2]/sum*totalToBet*bankroll/bett[3]-bett[4]
    
    for i in bets:
        print i    




if __name__ == "__main__":
    league = League()
    
    league.teamsFromFile("data\\teamsData.csv")
    league.buildFromFile("data\\gamesData.csv")
    league.purge()
    league.gradientDescent(10.0**-12.0)