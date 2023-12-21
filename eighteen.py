import time
import logging
import argparse

from pathlib import Path


class DigDug:

    def __init__(self, raw_data):

        self.dig_plan = self.parse_plan(raw_data)

        self.site = []


    def parse_plan(self, raw_data):

        lines = raw_data.split('\n')

        out = []

        for line in lines:

            parts = line.split()

            direction = parts[0]
            count = int(parts[1])
            rgb = parts[2].strip('()').replace('#','')

            out.append((direction, count, rgb))

        return out


    def hex_pit_vol(self):

        look = ('R','D','L','U')

        ridx, cidx = 0, 0

        ranges = []

        for inst in self.dig_plan:

            _, _, rgb = inst

            head = int(rgb[-1])
            dist = int(rgb[:-1], 16)

            logging.debug('%s -> %s @ %s', rgb, look[head], dist)

            if look[head] == 'R':
                ranges.append((ridx,cidx))
                cidx += dist

            if look[head] == 'L':
                ranges.append((ridx, cidx))
                cidx -= dist

            if look[head] == 'U':
                ranges.append((ridx, cidx))
                ridx -= dist

            if look[head] == 'D':
                ranges.append((ridx, cidx))
                ridx += dist

        ridxes = []
        cidxes = []

        logging.debug('RANGES: %s', ranges)

        for ranje in ranges:

            ridx, cidx = ranje

            ridxes.append(ridx)
            cidxes.append(cidx)

        rmin = min(ridxes)
        rmax = max(ridxes)
        cmin = min(cidxes)
        cmax = max(cidxes)

        logging.debug('MIN/MAX: R: %s/%s C: %s/%s', rmin, rmax, cmin, cmax)

        # For each row from rmin to rmax
        # Find any ranjes on that row
        # Count the borders, including 'U' and 'S' shapes, and calculate the insides

        for ridx in range(rmax-rmin):

            relevants = []

            # Find relevant ranges:
            for ranj in ranges:
                if ranj[0] == ridx and ranj not in relevants:
                    relevants.append(ranj)

            rel_cidx = []
            for coords in relevants:
                for ranj in ranges:
                    if coords[1] == ranj[1] and ranj not in relevants:
                        rel_cidx.append(ranj)

            relevants += rel_cidx
            logging.debug('RELEVANTS: %s', relevants)

            # From the left, find the first boundary (lowest cidx)
            # Count boundary hashes toward total
            # Check above and below for hash
            #  - If both, inside is True

            # Leftmost boundary
            minc = min(relevants, key=lambda x: x[1])[1]
            logging.debug('MINC: %s', minc)

            above = False
            below = False
            for relr, relc in relevants:
                if relc == minc:
                    if (ridx - 1) >= relr:
                        above = True
                    if (ridx + 1) <= relr:
                        below = True
            logging.debug('ABOVE/BELOW: %s/%s', above, below)

            if above and below:
                inside = True

            break


    def pit_volume(self):

        ridx, cidx = 0, 0

        pit = []
        pit.append((ridx,cidx))

        nmap = {
                'U': (-1,  0),
                'D': ( 1,  0),
                'L': ( 0, -1),
                'R': ( 0,  1),
                }

        for inst in self.dig_plan:

            head, count, _ = inst

            for i in range(1, count+1):

                ridx += nmap[head][0]
                cidx += nmap[head][1]

                pit.append((ridx,cidx))

        min_r = min(pit, key=lambda x: x[0])[0]
        max_r = max(pit, key=lambda x: x[0])[0]
        min_c = min(pit, key=lambda x: x[1])[1]
        max_c = max(pit, key=lambda x: x[1])[1]

        logging.debug('(%s,%s) MINR.MAXR / MINC.MAXC -> %s.%s / %s.%s', ridx, cidx, min_r, max_r, min_c, max_c)

        self.site = [['.' if ((ridx+min_r),(cidx+min_c)) not in pit else '#' for cidx in range(abs(max_c-min_c)+1)] for ridx in range(abs(max_r-min_r)+1)]
        #logging.debug('SITE: \n%s', '\n'.join([''.join(row) for row in self.site]))
        site = '\n'.join([''.join(row) for row in self.site])
        with open('site_before.txt','w') as f:
            f.write(site)

        total_vol = 0

        #logging.debug('SITE: %s', self.site)
        insides = []
        for ridx, row in enumerate(self.site):

            inside = False
            opn = False
            above, below = False, False
            for cidx, char in enumerate(row):

                #logging.debug('(%s,%s) -> %s', ridx, cidx, char)
                if char == '#':
                    total_vol += 1

                    if ridx - 1 >= 0:
                        if self.site[ridx-1][cidx] == '#':
                            above = not above

                    if ridx + 1 < len(self.site):
                        if self.site[ridx+1][cidx] == '#':
                            below = not below

                    if above and below:
                        inside = True
                    else:
                        inside = False

                else:
                    if inside:
                        insides.append((ridx,cidx))
                        #self.site[ridx][cidx] = '#'
                        total_vol += 1

        for pair in insides:
            ridx, cidx = pair
            self.site[ridx][cidx] = '#'

        site = '\n'.join([''.join(row) for row in self.site])
        with open('site_after.txt','w') as f:
            f.write(site)

        return total_vol


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 18', epilog='https://adventofcode.com')
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

    dd = DigDug(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        total_vol = dd.pit_volume()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', total_vol, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        total_vol = dd.hex_pit_vol()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', total_vol, round(end - start, 4))

