import time
import logging
import argparse

from functools import lru_cache
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

    def str_join(self, int_list):
        if not int_list:
            return ''
        return ','.join([str(i) for i in int_list])


    def str_unjoin(self, joined_str):
        if not joined_str:
            return []
        return [int(i) for i in joined_str.split(',')]


    #@lru_cache
    def recurse(self, record, contiguous):

        contiguous = self.str_unjoin(contiguous)

        total = 0
        logging.debug('RECORD: %s -> %s', record, contiguous)

        if contiguous:
            if not record or ('#' not in record and '?' not in record):
                logging.debug('END')
                return 0

        if not contiguous:
            if '#' in record:
                logging.debug('END')
                return 0
            else:
                logging.debug('TOTAL+1')
                return 1

        segments = self.get_record_segments(record)
        logging.debug('SEGMENTS: %s', segments)

        char, count = segments[0]
        while segments[0][0] == '.':
            record = record[count:]
            segments.pop(0)
            if not segments and contiguous:
                logging.debug('SEG END')
                return 0
            char, count = segments[0]

        if char == '?':
            # I think (?) we want to try all possibilities off '?' * count in recursion
            logging.debug('Branch 1 [RECx%s]', 2**count)
            for bin_str in self.possible_combos(count):
                n_record = bin_str + record[count:]
                total += self.recurse(n_record, self.str_join(contiguous))

        if char == '#':
            logging.debug('Branch 2')
            if count == contiguous[0]:
                # Item following consumed group must be a '.' or a '?' interpreted as a '.',
                # otherwise the contiguous group is actually larger than the value consumed.
                logging.debug('Branch 2.1 [REC]')
                if len(segments) > 1:
                    if segments[1][0] == '.':
                        logging.debug('Branch 2.1.1 [REC]')
                        n_record = record[count:]
                        return self.recurse(n_record, self.str_join(contiguous[1:]))
                    if segments[1][0] == '?':
                        logging.debug('Branch 2.1.2 [REC]')
                        n_record = '.' + record[count+1:]
                        return self.recurse(n_record, self.str_join(contiguous[1:]))
                return 1

            if count < contiguous[0]: #and len(segments) > 1 and segments[1][0] == '?':
                logging.debug('Branch 2.2 [REC]')
                num_fseg = 1
                pot_cont = count
                while pot_cont < contiguous[0] and len(segments) > num_fseg and segments[num_fseg][0] != '.':
                    # While future segments are alternating '?' and '#', turn the '?' into '#' until contig value is satisfied
                    pot_cont += segments[num_fseg][1]
                    num_fseg += 1

                if pot_cont > count:
                    n_record = ('#' * contiguous[0]) + record[contiguous[0]:]
                    return self.recurse(n_record, self.str_join(contiguous))

            if count > contiguous[0]:
                logging.debug('Branch 2.3')
                return 0

            logging.debug('END')

        return total


    def brute_force(self, record, contiguous):

        # For each '?' in a record, what does it become, a '.' or a '#',
        # in order to satisfy the contiguous counts?

        valids = []

        contiguous = self.str_unjoin(contiguous)

        num_unknown = record.count('?')
        segments = self.get_record_segments(record)

        test_record = ''
        for bin_val in self.possible_combos(num_unknown):
            logging.debug('BIN_VAL: %s', bin_val)

            ridx = 0
            for segment in segments:
                char, count = segment
                if char in ['.','#']:
                    test_record += char * count
                else:
                    logging.debug('BIN_VAL[%s:%s] = %s', ridx, (ridx+count), bin_val[ridx:ridx+count])
                    test_record += bin_val[ridx:ridx+count]
                    ridx += count

            if self.validate_record(test_record, contiguous):
                logging.debug('VALID: %s', test_record)
                valids.append(test_record)
            else:
                logging.debug('INVALID: %s', test_record)

            test_record = ''

        logging.debug('Record: %s %s -> %s', record, contiguous, len(valids))
        return len(valids)


    @lru_cache
    def possible_combos(self, str_len):

        combos = []
        for i in range(2**str_len):
            bin_val = format(i, f'0{str_len}b').replace('0','.').replace('1','#')
            combos.append(bin_val)

        return combos


    def sum_possibles(self, use_func, mult=1, max_records=0):

        logging.debug('Summing possibilities for %s records', len(self.records))

        total = 0

        for ridx, record in enumerate(self.records):

            logging.debug(' --- Processing Record %s --- ', ridx)

            record, contiguous = record

            record = '?'.join([record] * mult)
            contiguous = contiguous * mult

            contiguous = self.str_join(contiguous)

            valids = use_func(record, contiguous)
            logging.debug('Total + %s', valids)
            total += valids

            if max_records > 0:
                if (ridx + 1) == max_records:
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
        start = time.time()
        poss_sum = sr.sum_possibles(sr.recurse)
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', poss_sum, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        poss_sum = sr.recurse(sr.records[5][0], sr.str_join(sr.records[5][1]))
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', poss_sum, round(end - start, 4))

