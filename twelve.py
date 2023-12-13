import logging
import argparse

from pathlib import Path

class SpringRecords:

    def __init__(self, raw_data):

        self.records = []
        self.parse_records(raw_data)


    def parse_records(self, raw_data):

        for line in raw_data.split('\n'):

            record, contigs = line.split()
            contig_list = [int(x) for x in contigs.split(',')]

            self.records.append((record, contig_list))


    def get_record_segments(self, record):

        segments = []

        for char in record:

            if not segments:
                segments.append([char, 1])
                continue

            if segments[-1][0] == char:
                segments[-1][1] += 1
            else:
                segments.append([char, 1])

        return segments


    def validate_record(self, record, contiguous):

        if '?' in record:
            logging.error('Cannot validate record containing "?": %s', record)
            return

        segments = self.get_record_segments(record)
        cidx = 0

        for segment in segments:
            char, count = segment
            logging.debug('CHAR: %s COUNT: %s CIDX: %s', char, count, cidx)
            if char == '#':
                if cidx < len(contiguous) and count == contiguous[cidx]:
                    cidx += 1
                else:
                    return False

        logging.debug('LEN(CONT): %s + 1 < %s', cidx, len(contiguous))
        if cidx < len(contiguous):
            return False

        return True


    def calculate_arrangements(self, record, contiguous):

        hashes = ['#'*i for i in contiguous]

        # all hashes must fit in all groups of question marks
        # each hash string must be separated by one or more '.'
        # a hash string may overwrite other hashes or question marks, but not dots
        # hash strings must maintain original order
        # a hash string longer than a set of question marks cannot fit, assuming '.'s on each side

        segments = self.get_record_segments(record)
        num_qmarks = 0
        for char, count in segments:
            if char == '?':
                num_qmarks += 1

        # 1. Can first hash str fit in first qm group?
        #  - Yes: do it, and add a dot if there is room
        #  - No: first qm group is replaced by dots
        # 2. Can next hash str fit in current qm group?
        #  - Yes: do it, and add a dot


    def recurse(self, record, contiguous):

        total = 0
        logging.info('RECORD: %s -> %s', record, contiguous)

        segments = self.get_record_segments(record)
        logging.debug('SEGMENTS: %s', segments)

        if not contiguous and '?' not in record and '#' not in record:
            return 1

        char, count = segments[0]
        while segments[0][0] == '.':
            record = record[count:]
            segments.pop(0)
            char, count = segments[0]

        if char == '?':
            logging.debug('Branch 1')
            if count == 1:
                logging.debug('Branch 1.1 [REC]')
                n_record = '#' + record[1:]
                total += self.recurse(n_record, contiguous)
            else:
                logging.debug('Branch 1.2 [REC]')
                n_record = '#.' + record[2:]
                total += self.recurse(n_record, contiguous)

        if char == '#':
            logging.debug('Branch 2')
            if count == contiguous[0]:
                logging.debug('Branch 2.1 [REC]')
                n_record = record[count:]
                total += self.recurse(n_record, contiguous[1:])
            if count < contiguous[0] and len(segments) > 1 and segments[1][0] == '?' and segments[1][1] + count > contiguous[0]:
                logging.debug('Branch 2.2 [REC]')
                n_record = record[contiguous[0]+1:]
                total += self.recurse(n_record, contiguous[1:])

        return total


    def brute_force(self, record, contiguous):

        # For each '?' in a record, what does it become, a '.' or a '#',
        # in order to satisfy the contiguous counts?

        valids = []

        num_unknown = record.count('?')
        segments = self.get_record_segments(record)

        test_record = ''
        for i in range(2**num_unknown):
            bin_val = format(i, f'0{num_unknown}b')
            logging.debug('BIN_VAL: %s', bin_val)

            ridx = 0
            for segment in segments:
                char, count = segment
                if char in ['.','#']:
                    test_record += char * count
                else:
                    logging.debug('BIN_VAL[%s:%s] = %s', ridx, (ridx+count), bin_val[ridx:ridx+count])
                    test_record += bin_val[ridx:ridx+count].replace('0','.').replace('1','#')
                    ridx += count

            if self.validate_record(test_record, contiguous):
                logging.debug('VALID: %s', test_record)
                valids.append(test_record)
            else:
                logging.debug('INVALID: %s', test_record)

            test_record = ''

        logging.info('Record: %s %s -> %s', record, contiguous, len(valids))
        return len(valids)


    def sum_possibles(self, use_func, mult=1):

        logging.info('Summing possibilities for %s records', len(self.records))

        total = 0

        for ridx, record in enumerate(self.records):

            logging.info(' --- Processing Record %s --- ', ridx)

            record, contiguous = record

            record = '?'.join([record] * mult)
            contiguous = contiguous * mult

            valids = use_func(record, contiguous)
            logging.info('Total + %s', valids)
            total += valids

            if ridx == 1:
                break

        return total


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 12', epilog='https://adventofcode.com')
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

    sr = SpringRecords(data_in)

    ##
    # Part 1
    if not conf.p2:
        poss_sum = sr.sum_possibles(sr.brute_force)
        logging.info('[Part 1] Solution: %s', poss_sum)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        poss_sum = sr.sum_possibles(sr.recurse, mult=5)
        logging.info('[Part 2] Solution: %s', poss_sum)

