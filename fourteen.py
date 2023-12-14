import time
import logging
import argparse

from functools import lru_cache
from pathlib import Path


class MirrorRocks:

    def __init__(self, raw_data):

        self.rock_map = self.parse_rocks(raw_data)


    def __repr__(self):
        return '\n' + self.rock_str(self.rock_map)


    def rock_str(self, rock_map):
        return '\n'.join(rock_map)


    def parse_rocks(self, raw_data):
        return raw_data.split('\n')


    @lru_cache
    def tilt_north(self, rock_map):
        logging.debug('PRE-TILT: \n%s', rock_map)
        rock_map = self.parse_rocks(rock_map)

        for ridx, row in enumerate(rock_map):

            for cidx, char in enumerate(row):

                if ridx == 0:
                    continue

                if char == 'O':

                    roff = 0
                    while rock_map[ridx-1-roff][cidx] == '.' and (ridx - 1 - roff) >= 0:

                        rock_map[ridx-1-roff] = rock_map[ridx-1-roff][:cidx] + 'O' + rock_map[ridx-1-roff][cidx+1:]
                        rock_map[ridx-roff] = rock_map[ridx-roff][:cidx] + '.' + rock_map[ridx-roff][cidx+1:]

                        roff += 1

        rock_map = self.rock_str(rock_map)
        logging.debug('TILTED: \n%s', rock_map)
        return rock_map


    @lru_cache
    def tilt_south(self, rock_map):
        logging.debug('PRE-TILT: \n%s', rock_map)
        rock_map = self.parse_rocks(rock_map)

        for ridx in range(len(rock_map)-1, -1, -1):

            row = rock_map[ridx]

            for cidx, char in enumerate(row):

                if ridx == len(rock_map) - 1:
                    continue

                if char == 'O':

                    roff = 0
                    while (ridx + 1 + roff) < len(rock_map) and rock_map[ridx+1+roff][cidx] == '.':

                        rock_map[ridx+1+roff] = rock_map[ridx+1+roff][:cidx] + 'O' + rock_map[ridx+1+roff][cidx+1:]
                        rock_map[ridx+roff] = rock_map[ridx+roff][:cidx] + '.' + rock_map[ridx+roff][cidx+1:]

                        roff += 1

        rock_map = self.rock_str(rock_map)
        logging.debug('TILTED: \n%s', rock_map)
        return rock_map


    @lru_cache
    def tilt_east(self, rock_map):
        logging.debug('PRE-TILT: \n%s', rock_map)
        rock_map = self.parse_rocks(rock_map)

        for ridx, row in enumerate(rock_map):

            for cidx in range(len(row) - 1, -1, -1):

                char = row[cidx]

                if cidx == len(row) - 1:
                    continue

                if char == 'O':

                    coff = 0
                    while (cidx + 1 + coff) < len(row) and rock_map[ridx][cidx+1+coff] == '.':

                        rock_map[ridx] = rock_map[ridx][:cidx+1+coff] + 'O' + rock_map[ridx][cidx+2+coff:]
                        rock_map[ridx] = rock_map[ridx][:cidx+coff] + '.' + rock_map[ridx][cidx+1+coff:]

                        coff += 1

        rock_map = self.rock_str(rock_map)
        logging.debug('TILTED: \n%s', rock_map)
        return rock_map


    @lru_cache
    def tilt_west(self, rock_map):
        logging.debug('PRE-TILT: \n%s', rock_map)
        rock_map = self.parse_rocks(rock_map)

        for ridx, row in enumerate(rock_map):

            for cidx, char in enumerate(row):

                if cidx == 0:
                    continue

                if char == 'O':

                    coff = 0
                    while (cidx - 1 - coff) >= 0 and rock_map[ridx][cidx-1-coff] == '.':

                        rock_map[ridx] = rock_map[ridx][:cidx-1-coff] + 'O' + rock_map[ridx][cidx+1-coff:]
                        rock_map[ridx] = rock_map[ridx][:cidx-coff] + '.' + rock_map[ridx][cidx-coff:]

                        coff += 1

        rock_map = self.rock_str(rock_map)
        logging.debug('TILTED: \n%s', rock_map)
        return rock_map


    def spin_cycle(self, spin_count):

        order = [self.tilt_north, self.tilt_west, self.tilt_south, self.tilt_east]

        rock_map = self.rock_str(self.rock_map)

        for i in range(spin_count):

            for func in order:
                logging.debug('FUNC: %s', func)
                rock_map = func(rock_map)

        self.rock_map = self.parse_rocks(rock_map)
        logging.info('SPUN: %s', self)


    def calculate_load(self):

        total_weight = 0

        for ridx, row in enumerate(self.rock_map):
            rock_weight = len(self.rock_map) - ridx

            for char in row:

                if char == 'O':
                    total_weight += rock_weight

        return total_weight


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 14', epilog='https://adventofcode.com')
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

    mr = MirrorRocks(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        mr.rock_map = mr.parse_rocks(mr.tilt_north(mr.rock_str(mr.rock_map)))
        total_load = mr.calculate_load()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', total_load, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        mr.spin_cycle(1000000000)
        total_load = mr.calculate_load()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', total_load, round(end - start, 4))

