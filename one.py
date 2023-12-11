import logging
import argparse

from pathlib import Path


def find_num(line, alpha=False, rev=False):

    logging.debug('ARGS: %s / %s / %s', line, alpha, rev)

    swap_map = {
            'one': 1,
            'two': 2,
            'three': 3,
            'four': 4,
            'five': 5,
            'six': 6,
            'seven': 7,
            'eight': 8,
            'nine': 9,
            'zero': 0
            }

    idx = 0
    numval = None
    numidx = None

    for idx in range(len(line)):

        try:
            int(line[idx])
        except ValueError:
            idx += 1
        else:
            if numidx is None or (rev and idx > numidx) or (not rev and idx < numidx):
                numval = int(line[idx])
                numidx = idx

    #print(f'FOUND: {numval} @ {numidx}')

    alphval = None
    alphidx = None

    if alpha:

        for alpha in swap_map:

            # If rev, find last one, else first one
            if rev:
                for i in range(len(line), 0, -1):
                    found = line.find(alpha, i)
                    if found > -1:
                        break
            else:
                found = line.find(alpha)

            logging.debug('FOUND: %s @ %s', swap_map[alpha], found)

            if found > -1:

                if alphidx is None:
                    alphidx = found
                    alphval = swap_map[alpha]
                    continue

                if rev:
                    if found > alphidx:
                        alphval = swap_map[alpha]
                        alphidx = found
                else:
                    if found < alphidx:
                        alphval = swap_map[alpha]
                        alphidx = found

    logging.debug('NUM: %s @ %s', numval, numidx)
    logging.debug('ALPH: %s @ %s', alphval, alphidx)

    if alphidx is not None:

        if numidx is None:
            return alphval

        if rev:
            if alphidx > numidx:
                return alphval
            if numidx > alphidx:
                return numval
        else:
            if alphidx < numidx:
                return alphval
            if numidx < alphidx:
                return numval

    if numidx is not None:

        return numval

    raise Exception(f'No number found: {line}')


def lines_total(lines, alpha=False):

    sum_total = 0

    for line_no, line in enumerate(lines):

        if not line:
            continue

        logging.debug('LINE: %s', line)

        first = find_num(line, alpha=alpha)
        last = find_num(line, alpha=alpha, rev=True)

        num = int(f'{first}{last}')
        logging.debug('ANS: %s', num)
        logging.debug('---')
        sum_total += num

    return sum_total


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 1', epilog='https://adventofcode.com')
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

    lines = data_in.split('\n')

    ##
    # Part 1
    if not conf.p2:

        sum_total = lines_total(lines)
        logging.info('[Part 1] Sum total: %s' % sum_total)

    ###
    ## Part 2
    if not conf.p1 or conf.p2:

        sum_total = lines_total(lines, alpha=True)
        logging.info('[Part 2] Sum total: %s' % sum_total)
