#!/usr/bin/python3

import logger
import conf

def __usage_iosim():
    print("""\
Usage: iosim.py [<options>] <path>
  <options>
   -h: help(this message)
   -c <size in blks>
   -t <storage type>: default(no prefetch, lru), prefetch
   -i <interval>
   -d <bmp dim>
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
