import time
import logging
import argparse

from pathlib import Path


class PseudoCircuit:

    def __init__(self, raw_data):

        self.modules = {}

        self.state = {}
        self.inputs = {}
        self.outputs = {}

        self.frequency = {}
        self.cycles = 0
        self.presses = 0

        self.pulses = {
                'lo': 0,
                'hi': 0,
                }

        self.parse_schematic(raw_data)
        self.init_circuit()


    def parse_schematic(self, raw_data):

        lines = raw_data.split('\n')

        for line in lines:

            parts = line.split(' -> ')
            dests = parts[1].split(', ')

            if parts[0] == 'broadcaster':
                func = '|'
                label = parts[0]
            else:
                func = parts[0][0]
                label = parts[0][1:]

            self.modules[label] = tuple([func] + dests)

        logging.debug('MODULES: %s', self.modules)


    def init_circuit(self):

        self.state = {}
        self.inputs = {}
        self.outputs = {}
        self.pulses = {
                'lo': 0,
                'hi': 0,
                }

        self.frequency = {}
        self.cycles = 0
        self.presses = 0

        conj_list = []
        for label in self.modules:

            if self.modules[label][0] == '&':
                self.state.setdefault(label, {})
                conj_list.append(label)

            if self.modules[label][0] == '%':
                self.state.setdefault(label, False)

        orphans = []
        for label in self.modules:
            for target in self.modules[label][1:]:
                if target in conj_list:
                    self.state[target].setdefault(label, False)
                if target not in self.modules:
                    orphans.append(target)

        for orphan in orphans:
            self.modules.setdefault(orphan, ('*',))


    def process_queue(self):

        self.presses += 1

        while any(self.inputs.values()):

            logging.debug('--- ITER ---')

            self.outputs = {}
            self.cycles += 1

            for label in self.inputs:

                self.frequency.setdefault(label, {'hi': 0, 'lo': 0})

                func = self.modules[label][0]
                targets = self.modules[label][1:]

                for caller, insig in self.inputs[label]:
                    if insig:
                        self.frequency[label]['hi'] += 1
                        self.pulses['hi'] += 1
                    else:
                        self.frequency[label]['lo'] += 1
                        self.pulses['lo'] += 1

                    logging.debug('IN: %s[%s] -> %s[%s] -> %s', caller, insig, label, func, targets)

                    if func == '|':
                        outsig = False

                    if func == '*':
                        if label == 'rx' and insig is False:
                            return 'RX'
                        logging.debug('MODULE[OUTPUT]: <- %s', insig)

                    if func == '%':
                        mem = self.state[label]
                        if insig is True:
                            logging.debug('%%%s[%s] IGNORED', label, insig)
                            continue
                        else:
                            self.state[label] = not mem
                            outsig = self.state[label]

                    if func == '&':
                        self.state[label][caller] = insig
                        if all(self.state[label].values()):
                            outsig = False
                        else:
                            outsig = True

                    for target in targets:
                        self.outputs.setdefault(target, [])

                        send = (label, outsig)
                        self.outputs[target].append(send)
                        logging.debug('OUT: %s[%s] -> %s', label, outsig, target)

            self.inputs = {}

            for label in self.outputs:
                self.inputs.setdefault(label, self.outputs[label])

        logging.debug('OUT: %s', self.outputs)


    def ze_button(self, times=1):

        logging.debug('PRESS ZE BUTTON %sx', times)
        self.init_circuit()

        for _ in range(times):
            self.inputs.setdefault('broadcaster', [])
            self.inputs['broadcaster'].append(('button', False))
            self.process_queue()

        if times < 0:
            while True:
                self.inputs.setdefault('broadcaster', [])
                self.inputs['broadcaster'].append(('button', False))
                try:
                    if (self.frequency['th']['hi'] > 0 and
                            self.frequency['su']['hi'] > 0 and
                            self.frequency['gh']['hi'] > 0 and
                            self.frequency['ch']['hi'] > 0):
                        logging.info('FREQ / PRESSES: %s / CYCLES: %s', self.presses, self.cycles)
                        logging.info(self.frequency)
                        return self.presses
                except KeyError:
                    pass
                if self.process_queue() is not None:
                    return self.presses

        hi = self.pulses['hi']
        lo = self.pulses['lo']
        multi = hi * lo

        logging.debug('PULSES // HI: %s / LO: %s / MULT: %s', hi, lo, multi)

        return multi


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 20', epilog='https://adventofcode.com')
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

    pc = PseudoCircuit(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        pulses = pc.ze_button(times=1000)
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', pulses, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        pulses = pc.ze_button(times=-1)
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', pulses, round(end - start, 4))

