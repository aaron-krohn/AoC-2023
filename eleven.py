import time
import logging
import argparse

from pathlib import Path


class GalaxyMap:

    def __init__(self, raw_data):

        self.map = []
        self.galaxies = []
        self.empty_rows = []
        self.empty_cols = []
        self.exp_rate = 0

        self.parse_map(raw_data)
        self.expand()
        self.find_galaxies()


    def __repr__(self):

        return '\n' + '\n'.join([''.join(row) for row in self.map])


    def parse_map(self, raw_data):

        rows = raw_data.split('\n')
        self.map = [list(row) for row in rows]


    def find_galaxies(self):

        for ridx, row in enumerate(self.map):
            for cidx, space in enumerate(row):
                if space == '#':
                    self.galaxies.append((ridx,cidx))


    def nearest_galaxy(self, ridx, cidx):
        '''Not actually used in the challenges. Finds nearest galactic neighbor.
        '''

        nearest = None
        ndist = None

        for galaxy in self.galaxies:

            if galaxy == (ridx,cidx):
                continue

            dist = self.distance((ridx,cidx), galaxy)

            if nearest is None or dist < ndist:
                nearest = galaxy
                ndist = dist

        return nearest, ndist


    def distance(self, one, two):
        '''Find the number of empty rows and columns in between the two coordinate pairs.
           Multiply these values by current rate of expansion to find the total vertical
           and horizontal distances between points.
        '''

        rtot = 0
        for erow in self.empty_rows:
            if (erow > one[0] and erow < two[0]) or (erow < one[0] and erow > two[0]):
                rtot += 1

        ctot = 0
        for ecol in self.empty_cols:
            if (ecol > one[1] and ecol < two[1]) or (ecol < one[1] and ecol > two[1]):
                ctot += 1

        rtot = rtot * (self.exp_rate - 1)
        ctot = ctot * (self.exp_rate - 1)
        dist = abs(one[0] - two[0]) + abs(one[1] - two[1]) + ctot + rtot
        logging.debug('abs(%s-%s) + abs(%s-%s) + %s + %s = %s', one[0], two[0], one[1], two[1], rtot, ctot, dist)
        return dist


    def sum_distances(self):
        '''Find distance between all galaxy pairs.
        '''

        pairs = 0
        total = 0
        done = []

        for gal in self.galaxies:

            done.append(gal)

            for ogal in self.galaxies:

                if ogal in done:
                    continue

                pairs += 1

                dist = self.distance(gal, ogal)
                logging.debug('%s -> %s = %s', gal, ogal, dist)
                total += dist

        logging.info('Galaxy pairs: %s', pairs)
        return total


    def expand(self, exp_rate=1):
        '''Initially used to literally expand the map, but part 2 made this impossible.
           It still finds empty columns and rows for use in distance calculations
        '''

        self.empty_rows = []
        self.empty_cols = []

        self.exp_rate = exp_rate

        for ridx, row in enumerate(self.map):

            empty = True
            for spot in row:
                if spot != '.':
                    empty = False
                    break

            if empty:
                self.empty_rows.append(ridx)

        for cidx in range(len(self.map[0])):
            empty = True
            for row in self.map:

                if row[cidx] != '.':
                    empty = False
                    break

            if empty:
                self.empty_cols.append(cidx)

        logging.debug('EROWS: %s', self.empty_rows)
        logging.debug('ECOLS: %s', self.empty_cols)

        # for i, ecol in enumerate(self.empty_cols):
        #     for ridx, row in enumerate(self.map):
        #         self.map[ridx].insert(i+ecol, '.')

        # for i, erow in enumerate(self.empty_rows):
        #     row = '.' * len(self.map[0])
        #     self.map.insert(i+erow, row)


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 11', epilog='https://adventofcode.com')
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

    galaxies = GalaxyMap(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        galaxies.expand(2)
        dist_sum = galaxies.sum_distances()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', dist_sum, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        galaxies.expand(1000000)
        dist_sum = galaxies.sum_distances()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', dist_sum, round(end - start, 4))

