import time
import logging
import argparse

from functools import lru_cache
from pathlib import Path


class GardenMap:

    def __init__(self, raw_data):

        self.map = self.parse_data(raw_data)
        self.start = self.find_start()

        self.found = {}
        self.tried = {}


    def parse_data(self, raw_data):

        return raw_data.split('\n')


    def find_start(self):

        for ridx, row in enumerate(self.map):
            for cidx, char in enumerate(row):
                if char == 'S':
                    return (ridx, cidx)


    @lru_cache
    def take_steps(self, num_steps, ridx, cidx, inf=False):

        logging.debug('STEPS: %s @ %s', num_steps, (ridx, cidx))

        step_mask = {
                'N': (-1,  0),
                'E': ( 0,  1),
                'W': ( 0, -1),
                'S': ( 1,  0),
                }

        if num_steps == 0:
            if self.found.setdefault((ridx,cidx)) is None:
                logging.debug('GPLOTS+1')
                self.found[(ridx, cidx)] = True
            return

        for heading, mask in step_mask.items():
            nridx = ridx + mask[0]
            ncidx = cidx + mask[1]
            trying = f'{num_steps-1}@({nridx},{ncidx})'

            if inf is True:
                nridx = nridx % len(self.map)
                ncidx = ncidx % len(self.map[nridx])

            if trying not in self.tried and (self.map[nridx][ncidx] == '.' or self.start == (nridx, ncidx)):
                if inf is False:
                    if not (nridx >= 0 and nridx < len(self.map) and ncidx >= 0 and ncidx < len(self.map[ridx])):
                        continue

                self.tried.setdefault(trying, True)
                self.take_steps(num_steps-1, ridx+mask[0], cidx+mask[1], inf)

        return len(self.found)


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 21', epilog='https://adventofcode.com')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Show debug output')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use test input file')
    parser.add_argument('-p1', '--part-1', dest='p1', action='store_true', default=False, help='Only run part 1')
    parser.add_argument('-p2', '--part-2', dest='p2', action='store_true', default=False, help='Only run part 2, overrides -p1')
    parser.add_argument('-l', '--log', dest='logfile', action='store', help='Filename for writing log file')

    parsed = parser.parse_args()

    return parsed


if __name__ == '__main__':

    conf = parse_args()

    loglevel = logging.DEBUG if conf.debug else logging.INFO
    logging.basicConfig(level=loglevel, format='%(asctime)s [%(levelname)s] %(message)s', filename=conf.logfile)

    fn = [Path(__file__).stem, 'input']
    if conf.test:
        fn.insert(1, 'test')
    datafile = '.'.join(fn)

    with open(datafile, 'r') as f:
        data_in = f.read().strip()

    gm = GardenMap(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        num_gardens = gm.take_steps(64, gm.start[0], gm.start[1])
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', num_gardens, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        num_gardens = gm.take_steps(500, gm.start[0], gm.start[1], inf=True)
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', num_gardens, round(end - start, 4))

