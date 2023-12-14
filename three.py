import time
import logging
import argparse

from pathlib import Path


class Schematic:

    def __init__(self, schematic):

        self.schematic = schematic
        self.symbols = []

        self.find_symbols()


    def find_symbols(self):

        for yidx, row in enumerate(self.schematic):

            for xidx, char in enumerate(row):

                if char == '.':
                    continue

                try:
                    int(char)
                except ValueError:
                    symloc = (yidx, xidx)
                else:
                    continue

                self.symbols.append(symloc)


    def adjacent_parts(self, y, x):
        """Gets the part numbers adjacent to coordinates.
           Coordinates do not have to be the location of a symbol
        """
        logging.debug('Y,X: %s,%s = %s', y, x, self.schematic[y][x])

        parts = []

        # Neighbor pixel offsets
        locs = (
                (-1, -1), (-1, 0), (-1, 1),
                ( 0, -1),          ( 0, 1),
                ( 1, -1), ( 1, 0), ( 1, 1),
                )

        # Check each neighbor
        for yoff, xoff in locs:

            part_num = self.load_part_num(y+yoff, x+xoff)

            if part_num is not None and part_num not in parts:
                parts.append(part_num)

        return parts


    def load_part_num(self, y, x):
        """Loads a part number at given coordinates.
           Returns None if coordinates are not an int
        """

        try:
            num = str(int(self.schematic[y][x]))
        except ValueError:
            return None

        logging.debug('NUM: %s', num)

        xoff = -1
        while x + xoff >= 0 and x + xoff < len(self.schematic[y]):

            try:
                addleft = str(int(self.schematic[y][x+xoff]))
                logging.debug('LEFT: %s', addleft)
            except ValueError:
                break
            else:
                num = addleft + str(num)

            xoff -= 1

        xoff = 1
        while x + xoff >= 0 and x + xoff < len(self.schematic[y]):

            try:
                addright = str(int(self.schematic[y][x+xoff]))
                logging.debug('RIGHT: %s', addright)
            except ValueError:
                break
            else:
                num = str(num) + addright

            xoff += 1

        return int(num)


    def sum_sym_parts(self):

        total = 0

        for symy, symx in self.symbols:

            parts = self.adjacent_parts(symy, symx)
            if parts:
                total += sum(parts)

        return total


    def sum_gear_ratios(self):

        total = 0

        for symy, symx in self.symbols:

            if self.schematic[symy][symx] == '*':
                parts = self.adjacent_parts(symy, symx)
                if parts and len(parts) == 2:
                    total += parts[0] * parts[1]

        return total


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 3', epilog='https://adventofcode.com')
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

    schem_data = data_in.split('\n')
    schematic = Schematic(schem_data)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        parts_sum = schematic.sum_sym_parts()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', parts_sum, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        gr_sum = schematic.sum_gear_ratios()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', gr_sum, round(end - start, 4))

