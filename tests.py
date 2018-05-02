import unittest
import lolbet
import datetime
from leagueTests import *

class nCrTest(unittest.TestCase):

    def testNCr(self):
        self.failUnless(lolbet.nCr(4,2)== 6)

class winProbabilityFromDeltaEloTest(unittest.TestCase):

    def test5050(self):
        self.failUnless(lolbet.winProbabilityFromDeltaElo(0) == 0.5)

    def testInf(self):
        self.failUnless(lolbet.winProbabilityFromDeltaElo(200) == 1.0/(1.0+10.0**(-200.0/400.0)) )

class TeamClassTest(unittest.TestCase):

    def setUp(self):
        self.team = lolbet.Team("SoloMid")
        
    def testConstructor(self):
        self.failUnless(self.team.name == "SoloMid")

    def testStartingElo(self):
        self.failUnless(self.team.elo == 0)

    def testStartingResultsList(self):
        self.failUnless(self.team.resultsList == [])

class ResultClassTest(unittest.TestCase):

    def setUp(self):
        self.soloMid = lolbet.Team("SoloMid")
        self.cLG = lolbet.Team("CLG")
        self.date = datetime.date(2014,8,16)
        self.result = lolbet.Result(self.soloMid,self.cLG,1,self.date)
        
    def testAddToBlueResultsList(self):
        self.failUnless(self.result in self.soloMid.resultsList)

    def testAddToPurpleResultsList(self):
        self.failUnless(self.result in self.cLG.resultsList)

    def testTeamScore1(self):
        self.failUnless(self.result.scoreOfTeam(self.soloMid) == 1)

    def testTeamScore2(self):
        self.failUnless(self.result.scoreOfTeam(self.cLG) == 0)

    def testGetLoser(self):
        self.failUnless(self.result.getLoser() == self.cLG)

    def testGetOpponentOf(self):
        self.failUnless(self.result.getOpponentOf(self.cLG) == self.soloMid)

    def testGetSideOf1(self):
        self.failUnless(self.result.getSideOf(self.cLG) == "purple")

    def testGetSideOf2(self):
        self.failUnless(self.result.getSideOf(self.soloMid) == "blue")


class isConnectedByWinsTest(unittest.TestCase):

    def setUp(self):
        self.teamA = lolbet.Team("A")
        self.teamB = lolbet.Team("B")
        self.teamC = lolbet.Team("C")
        self.teamD = lolbet.Team("D")
        lolbet.Result(self.teamA,self.teamB,1,datetime.date(2014,8,16))
        lolbet.Result(self.teamA,self.teamB,0,datetime.date(2014,8,16))
        lolbet.Result(self.teamB,self.teamC,1,datetime.date(2014,8,16))
        lolbet.Result(self.teamC,self.teamD,1,datetime.date(2014,8,16))

    def testIsConnected(self):
        self.failUnless(self.teamA.isConnectedByWinsTo(self.teamD))

    def testIsNotConnected(self):
        self.failUnless(not(self.teamD.isConnectedByWinsTo(self.teamA)))

    def testGetWinsAgainstSet(self):
        self.failUnless(self.teamA.getTeamsBeatenSet() == set([self.teamB]))

    def testIsConnectedTo1(self):
        self.failUnless(self.teamA.isConnectedTo(self.teamB))

    def testIsConnectedTo2(self):
        self.failUnless(not(self.teamD.isConnectedTo(self.teamA)))

class gradientTests(unittest.TestCase):

    def setUp(self):
        self.teamA = lolbet.Team("A")
        self.teamB = lolbet.Team("B")
        self.teamB.elo+=30
        lolbet.Result(self.teamA,self.teamB,1,datetime.date(2014,8,16))
        lolbet.Result(self.teamA,self.teamB,0,datetime.date(2014,8,16))

    def testEven(self):
        self.failUnless(self.teamB.gradient(30,2) == 0)
    

class buildFromFileTests(unittest.TestCase):

    def setUp(self):
        self.league = lolbet.League()
        self.league.buildFromFile("data\\testResults.csv")

    def testTeamsAreThere1(self):
        self.failUnless(self.league.teamsDictionary.has_key("SHC XD"))

    def testTeamsAreThere2(self):
        self.failUnless(self.league.teamsDictionary.has_key("Millenium"))

    def testSideAreRight1(self):
        team = self.league.teamsDictionary["SHC XD"]
        self.failUnless(team.resultsList[0].getSideOf(team) == "blue")

    def testSideAreRight1(self):
        team = self.league.teamsDictionary["SHC XD"]
        self.failUnless(team.resultsList[1].getSideOf(team) == "purple")

    def testDateIsRight(self):
        team = self.league.teamsDictionary["SHC XD"]
        self.failUnless(team.resultsList[0].date == datetime.date(2014,8,14))

    def testWinnerIsRight(self):
        team = self.league.teamsDictionary["SHC XD"]
        self.failUnless(team.resultsList[0].scoreOfTeam(team) == 1)

    def testGetTeam(self):
        team = self.league.teamsDictionary["SHC XD"]
        self.failUnless(self.league.getTeam("SHC XD") == team)
        

class gradientDescentTest(unittest.TestCase):

    def setUp(self):
        self.league = lolbet.League()
        self.league.buildFromFile("data\\gamesData.csv")
        

class readTeamsFromFileTest(unittest.TestCase):
    
    def setUp(self):
        self.league = lolbet.League()
        self.league.teamsFromFile("data\\teamsFileTest.csv")

    def test1(self):
        self.failUnless(self.league.teamsDictionary["A"].elo == 1234.0)
        
    def test2(self):
        self.failUnless(self.league.teamsDictionary["B"].name == "B")
        
    def testSave(self):
        self.league.teamsToFile("data\\saveTest.csv")
        
        
        

        
def main():
    unittest.main()

if __name__ == '__main__':
    main()
