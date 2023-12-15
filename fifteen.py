import time
import logging
import argparse

from pathlib import Path

class Hasher:

    def __init__(self, raw_data):

        self.unhashed = self.parse_data(raw_data)

        self.boxes = [[] for _ in range(256)]


    def parse_data(self, raw_data):

        return raw_data.split(',')


    def hash_data(self, data):

        total = 0

        for char in data:
            total += ord(char)
            total = total * 17
            total = total % 256

        logging.debug('HASH(%s) = %s', data, total)

        return total


    def hash_sum(self):

        total = 0

        for item in self.unhashed:

            total += self.hash_data(item)

        return total


    def arrange_lenses(self):

        logging.debug('BOXES: %s', self.boxes)
        for inst in self.unhashed:

            logging.debug('INST: %s', inst)

            if '=' in inst:
                pair = inst.split('=')

                label = pair[0]
                fl = int(pair[1])
                box = self.hash_data(label)

                old_lens = None
                for idx, lens in enumerate(self.boxes[box]):
                    if lens[0] == label:
                        old_lens = self.boxes[box].pop(idx)
                        self.boxes[box].insert(idx, (label, fl))

                if old_lens is None:
                    self.boxes[box].append((label, fl))

            if inst[-1] == '-':

                label = inst[:-1]
                box = self.hash_data(label)

                for idx, lens in enumerate(self.boxes[box]):
                    if lens[0] == label:
                        self.boxes[box].pop(idx)

            logging.debug('BOXES: %s', self.boxes)


    def sum_focus_power(self):

        total = 0

        for bidx, box in enumerate(self.boxes):

            for lidx, lens in enumerate(box):

                total += (1 + bidx) * (lidx + 1) * lens[1]

        return total



def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 15', epilog='https://adventofcode.com')
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

    mr = Hasher(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        hash_sum = mr.hash_sum()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', hash_sum, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        mr.arrange_lenses()
        focus_sum = mr.sum_focus_power()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', focus_sum, round(end - start, 4))

