#!/usr/bin/python3

import logger
import conf

def __usage_iosim():
    print("""\
Usage: iosim.py [<options>] <trace path>
  <options>
   -h: help(this message)
   -c <size in blks>
   -t <storage type>: all, default(no prefetch, lru), prefetch, ml, rule
   -T <timestamp range>
  <options for rule>
   -p: enable per-process reference history (default: disabled)
   -b <count>: reference history count, (default: 1)
  <options for ml>
   -p: enable per-process reference history (default: enabled)
   -G <width(time) x height(lba)>: grid dimension (default: 5x10)
   -u <sec>: width unit for time (default: 0.005)
   -L <lba max>
   -m <model path>: for storage ml only
   -M <model type>: for storage ml only
""")

if __name__ == "__main__":
    from sim import Simulator

    logger.init("iosim")

    sim = Simulator()

    conf.parse(__usage_iosim)
    sim.run()
