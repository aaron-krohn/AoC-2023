import time
import logging
import argparse

from pathlib import Path

class LightGrid:

    def __init__(self, raw_data):

        self.grid = self.parse_grid(raw_data)

        self.energized = []

        self.threads = 1


    def parse_grid(self, raw_data):

        return raw_data.split('\n')


    def sim_path(self, start=(0,0), heading='right'):

        thread = self.threads
        self.threads += 1

        dir_offs = {
                'right': (0, 1),
                'left':  (0, -1),
                'up':    (-1, 0),
                'down':  (1, 0),
                }

        ridx, cidx = start

        while ridx >= 0 and cidx >= 0 and ridx < len(self.grid) and cidx < len(self.grid[0]):

            char = self.grid[ridx][cidx]
            self.energized.append((ridx, cidx, heading))

            logging.debug('[%s] (%s,%s) -> %s : %s', thread, ridx, cidx, heading, char)

            if char == '/':
                if heading == 'right':
                    heading = 'up'
                elif heading == 'left':
                    heading = 'down'
                elif heading == 'up':
                    heading = 'right'
                elif heading == 'down':
                    heading = 'left'

            if char == '\\':
                if heading == 'right':
                    heading = 'down'
                elif heading == 'left':
                    heading = 'up'
                elif heading == 'up':
                    heading = 'left'
                elif heading == 'down':
                    heading = 'right'


            if char == '|':
                if heading in ['right','left']:
                    nridx = ridx + dir_offs['up'][0]
                    ncidx = cidx + dir_offs['up'][1]
                    self.sim_path((nridx, ncidx), 'up')
                    heading = 'down'

            if char == '-':
                if heading in ['up','down']:
                    nridx = ridx + dir_offs['left'][0]
                    ncidx = cidx + dir_offs['left'][1]
                    self.sim_path((nridx, ncidx), 'left')
                    heading = 'right'

            ridx += dir_offs[heading][0]
            cidx += dir_offs[heading][1]

            if (ridx, cidx, heading) in self.energized:
                logging.debug('NOT REPEATING: (%s, %s) -> %s', ridx, cidx, heading)
                break


    def hash_count(self):

        items = []

        for item in self.energized:

            ridx, cidx, heading = item
            coords = (ridx, cidx)
            if coords not in items:
                items.append(coords)

        return len(items)


    def reset(self):

        self.threads = 1
        self.energized = []


    def max_energy(self):

        self.reset()

        maxe = 0

        for ridx in range(len(self.grid)):

            if ridx == 0:

                # cidx = 0
                tried_1 = self.sim_path((0,0), 'down')
                tried_2 = self.sim_path((0,0), 'right')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

                for cidx in range(1, len(self.grid[0]) - 1):
                    tried = self.sim_path((ridx,cidx), 'down')
                    hc = self.hash_count()
                    if hc > maxe:
                        maxe = hc
                    self.reset()

                tried_1 = self.sim_path((0,len(self.grid[0])-1), 'down')
                tried_2 = self.sim_path((0,len(self.grid[0])-1), 'left')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

            elif ridx == len(self.grid) - 1:

                # cidx = 0
                tried_1 = self.sim_path((0,0), 'up')
                tried_2 = self.sim_path((0,0), 'right')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

                for cidx in range(1, len(self.grid[0]) - 1):
                    tried = self.sim_path((ridx,cidx), 'up')
                    hc = self.hash_count()
                    if hc > maxe:
                        maxe = hc
                    self.reset()

                tried_1 = self.sim_path((0,len(self.grid[0])-1), 'up')
                tried_2 = self.sim_path((0,len(self.grid[0])-1), 'left')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

            else:

                tried = self.sim_path((ridx,0), 'right')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

                tried = self.sim_path((ridx,len(self.grid[0])-1), 'left')
                hc = self.hash_count()
                if hc > maxe:
                    maxe = hc
                self.reset()

        return maxe


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 16', epilog='https://adventofcode.com')
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

    lm = LightGrid(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        lm.sim_path()
        hash_sum = lm.hash_count()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', hash_sum, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        max_energy = lm.max_energy()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', max_energy, round(end - start, 4))

