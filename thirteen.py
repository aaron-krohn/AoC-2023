import logging
import argparse

from pathlib import Path


class LavaMirrors:

    def __init__(self, raw_data):

        self.notes = []
        self.meta = {}

        self.parse_notes(raw_data)


    def parse_notes(self, raw_data):

        notes_raw = raw_data.split('\n\n')

        for note in notes_raw:

            lines = note.split('\n')
            self.notes.append(lines)


    def rotate_note(self, note):

        rows = []

        for cidx in range(len(note[0])):
            col = ''
            for ridx in range(len(note)-1,-1,-1):
                col += note[ridx][cidx]
            rows.append(col)

        return rows


    def find_reflection(self, nidx, rote=False):

        note = self.notes[nidx]

        if rote:
            note = self.rotate_note(note)

        for ridx in range(len(note)-1):

            if note[ridx] == note[ridx+1]:

                if self.check_reflection(note, ridx):

                    if rote is False:
                        self.meta.setdefault(nidx, ('h', ridx))
                        return 100 * (ridx + 1)
                    else:
                        self.meta.setdefault(nidx, ('v', ridx))
                        return (ridx + 1)


    def check_reflection(self, note, ridx):

        mirror = True
        jidx = 0

        while ridx - jidx >= 0 and ridx + jidx + 1 < len(note):
            if note[ridx-jidx] != note[ridx+jidx+1]:
                mirror = False
                break

            jidx += 1

        return mirror


    def find_smudge(self, note):

        # A smudge is identical to another row/col, but off by one char
        # There are an even number of row/col between the two

        # Row containing the smudge
        for ridx in range(len(note)):

            # Row mirroring smudged row
            for idx, row in enumerate(note):

                if idx == ridx or row == note[ridx]:
                    continue

                offby = 0
                cidx = 0
                # Character index of the smudge
                for chx, char in enumerate(row):
                    if char != note[ridx][chx]:
                        offby += 1
                        cidx = chx

                #logging.debug('OFFBY: %s / RIDX: %s (%s) / IDX: %s (%s)', offby, ridx, note[ridx], idx, row)

                # To have an even number of rows between them, there is remainder 1:
                # e.g. There are 4 rows between indexes 0 and 5, thus abs(0-5) % 2 == 1
                if offby == 1 and abs(idx - ridx) % 2 == 1:
                    logging.debug('OFFBY: %s / MOD: abs(%s - %s)', offby, idx, ridx)
                    logging.debug('%s', row)
                    logging.debug('%s', note[ridx])

                    flipchr = '.' if note[ridx][cidx] == '#' else '#'
                    test_note = note[:]
                    test_note[ridx] = note[ridx][:cidx] + flipchr + note[ridx][cidx+1:]

                    # Where to check reflection
                    midx = int((((abs(ridx-idx) + 1) / 2) + min([ridx,idx])) - 1)
                    logging.debug('MIDX: %s', midx)

                    reflects = self.check_reflection(test_note, midx)
                    logging.debug('REFLECTS: %s', reflects)
                    if reflects:
                        refrow = midx + 1
                        logging.debug('VALUE: %s', refrow)
                        return refrow


    def note_totals(self):

        total = 0

        for idx in range(len(self.notes)):

            horiz = self.find_reflection(idx)

            if not horiz:
                vert = self.find_reflection(idx, rote=True)
                total += vert
            else:
                total += horiz

        logging.debug('META: %s', self.meta)
        return total


    def smudge_totals(self):

        total = 0

        for idx in range(len(self.notes)):


            note = [i[:] for i in self.notes[idx]]
            logging.debug('NOTE %s: %s %s', idx, self.meta[idx], self.note_string(note))

            logging.debug('Find HORIZ smudge')
            smudge = self.find_smudge(note)

            if not smudge:
                logging.debug('Find VERT smudge')
                note = self.rotate_note(note)
                logging.debug('NOTE %s: %s', idx, self.note_string(note))
                adding = self.find_smudge(note)
            else:
                adding = 100 * smudge

            logging.debug('%s = %s + %s', total, adding, (total+adding))
            total += adding

        return total


    def note_string(self, note):

        return '\n' + '\n'.join(note)


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 13', epilog='https://adventofcode.com')
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

    lm = LavaMirrors(data_in)

    ##
    # Part 1
    if not conf.p2:
        reflect_sum = lm.note_totals()
        logging.info('[Part 1] Solution: %s', reflect_sum)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        smudge_sum = lm.smudge_totals()
        logging.info('[Part 2] Solution: %s', smudge_sum)

