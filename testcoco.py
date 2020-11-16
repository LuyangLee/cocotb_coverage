from cocotb_coverage.coverage import *
from cocotb_coverage.crv import *
import logging
import cocotb

# example 1：
class Point(Randomized):
    def __init__(self, pdir=0, pdis=0):
        Randomized.__init__(self)
        # direction(0-1), distance(width), ptype(color)
        self.pdir = pdir
        self.pdis = pdis
        self.ptype = "red"

        ##################################
        # variables randomization setting #
        ##################################
        # define dir as a random variable taking values from 0 to 1,
        self.add_rand("pdir", [0,1])
        # define len as a random variable taking values from 1 to 64,
        self.add_rand("pdis", list(range(1, 65)))
        # define type as a random variable taking str from list
        self.add_rand("ptype", ["red","yellow","green"])

        ###########################
        # constraint randomization #
        ##########################
        # add constriant
        self.add_constraint(lambda  pdir, pdis:  32< pdis < 64 if pdir == 1 else pdis <= 32)
        # add constraint, P(pdis<10)=0.9, P(pdis>=10)=0.1
        self.add_constraint(lambda pdis: 0.9 if pdis < 10 else 0.1)
@CoverPoint(
    name = "top.p.direction",
    xf = lambda point: point.pdir,
    bins = [0, 1]
)
@CoverPoint(
    name = "top.p.dis",
    xf = lambda point: point.pdis,
    bins = list(range(1, 64))
)
def p_test(point):
    logging.info("direction is %d, distance is %d type is "+ point.ptype, point.pdir, point.pdis)


# example 2
class SimpleRandomized(Randomized):
    def __init__(self, x=0, y=0):
        Randomized.__init__(self)
        self.x = x
        self.y = y
        self.size = "small"

        self.add_rand("x", list(range(0, 10)))
        self.add_rand("y", list(range(0, 10)))
        self.add_rand("size", ["small", "medium", "large"])

        self.add_constraint(lambda x, y: x < y)

@CoverPoint(
    name = "top.sim.size",
    vname = "size",
    bins= ["small", "medium", "large"]
)
@CoverPoint(
    name = "top.sim.pair",
    xf   = lambda x, y, size: (x, y),
    bins = [(x,y) for x in range(0, 10) for y in range(x+1,10)],
)
@CoverCross(
    "top.sim.cross",
    items = ["top.sim.pair", "top.sim.size"],
    # small size(x=0~4 or y=0~4), medium size(x=5~7 or y=5~7), large size(x=8~9 or y=8~9)，but cocotb-coverage use ignore_bin in CoverCross, so use oppostite condition
    ign_bins= [((x, y), "small") for x in range(5, 10) for y in range(5, 10)] +
            [((x, y), "medium") for x in range(0, 5) for y in range(0, 5)] +
            [((x, y), "medium") for x in range(8, 10) for y in range(8, 10)] +
            [((x, y), "large") for x in range(0, 8) for y in range(0, 8)]
)
def simple_test(x, y, size):
    logging.info("(x, y) is (%d, %d), size " + size, x, y)

if __name__ == "__main__":
    # setting logging level
    logging.basicConfig(level=logging.DEBUG)
    for _ in range(10):
        p = Point()
        p.randomize()
        p_test(p)
        simple = SimpleRandomized()
        simple.randomize()
        simple_test(simple.x, simple.y, simple.size)
    coverage_db.report_coverage(logging.info, bins= False)


        


    