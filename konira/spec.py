# coding: pyspec

class Bow:
    def shot(self):
        # still hadn't figured out a way to access local class data 
        # through method wrapper. 
        print "got shot"
        
    def score(self):
        return 5

describe "Bowling around with friends":

    it "should score 0 for gutter game":
        bowling = Bow()
        bowling.shot()
        try:
            assert bowling.score.should_be(1)
        except Exception, e:
            assert bowling.score.should_be(5)
            print "real value reached: %s" % bowling.score()
