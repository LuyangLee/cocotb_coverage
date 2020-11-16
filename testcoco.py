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
# @CoverPoint(
#     name = "top.direction",
#     xf = lambda point: point.pdir,
#     bins = [0, 1]
# )
# @CoverPoint(
#     name = "top.dis",
#     xf = lambda point: point.pdis,
#     bins = list(range(1, 64)),
#     # rel = lambda val, b: b[0]< val <b[1]
# )
# def show(point):
#     logging.info("direction is %d, distance is %d type is "+ point.ptype, point.pdir, point.pdis)


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
    name = "top.x",
    xf   = lambda x, y, size: (x, y),
    bins = [(x,y) for x in range(0, 10) for y in range(x,10)],
)
def sim_show(x, y, size):
    logging.info("(x, y) is (%d, %d), size" + size, x, y)
if __name__ == "__main__":
    # setting logging level
    logging.basicConfig(level=logging.DEBUG)
    for _ in range(10):
        p = SimpleRandomized()
        p.randomize()
        sim_show(p.x, p.y, p.size)
    coverage_db.report_coverage(logging.info, bins= True)

        


    