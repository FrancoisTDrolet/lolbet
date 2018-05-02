import unittest
import lolbet
import datetime

class TestNewResultInputStr(unittest.TestCase):
    
    def setUp(self):
        self.league = lolbet.League()
        self.league.newResult("A","B",1,datetime.date(2014,9,11))
        
    def testTeamsAddedToDictionary(self):
        self.assertTrue(self.league.teamsDictionary.has_key("A") and self.league.teamsDictionary.has_key("B") )
        
    def testResultInList(self):
        self.assertFalse(self.league.resultsList == [])
        
    def testResultInBlue(self):
        self.assertFalse(self.league.getTeam("A").resultsList == [])
        
    def testResultInPurple(self):
        self.assertFalse(self.league.getTeam("B").resultsList == [])
        
    def testConvergence(self):
        self.league.newResult("A","B",1,datetime.date(2014,9,11))
        self.league.newResult("A","B",0,datetime.date(2014,9,11))
        teamA = self.league.getTeam("A")
        teamB = self.league.getTeam("B")
        self.league.gradientDescent(0.01,0)
        p = self.league.probabilityOfResult(teamA,teamB,1,0,1)
        self.assertTrue(p>0.65 and p<0.67)
        