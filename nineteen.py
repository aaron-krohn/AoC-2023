import time
import logging
import argparse

from pathlib import Path

class Workflow:

    def __init__(self, raw_data):

        self.parts = []
        self.workflows = {}

        self.parse_workflow_parts(raw_data)

        self.accepted = []


    def parse_workflow_parts(self, raw_data):

        raw_workflows, raw_parts = raw_data.split('\n\n')

        for part in raw_parts.split('\n'):
            pdata = {}
            for pair in part.strip('{}').split(','):
                key, val = pair.split('=')
                pdata.setdefault(key, int(val))
            self.parts.append(pdata)

        for workflow in raw_workflows.split('\n'):
            widx = workflow.index('{')
            wf_name = workflow[:widx]
            self.workflows.setdefault(wf_name, workflow[widx:])

        logging.debug('WORKFLOWS: %s', self.workflows)
        logging.debug('PARTS: %s', self.parts)


    def sum_parts(self):

        total = 0

        accepts = []

        for part in self.parts:

            if self.process_part(part) is True:
                logging.debug('ADD PART: %s', part)
                total += part['x'] + part['m'] + part['a'] + part['s']

        return total


    def all_conditions(self, wf=None):

        conditions = []

        if wf is None:
            wf = self.workflows['in']
        else:
            wf = self.workflows[wf]

        inst_list = wf.strip('{}').split(',')

        for inst in inst_list:

            if ':' in inst:
                cond, action = inst.split(':')
                cond = [cond]
            else:
                action = inst
                cond = []

            if action == 'R':
                continue
            elif action == 'A':
                conditions += cond
            else:
                conditions += cond + self.all_conditions(action)

        return conditions


    def all_acceptable(self):

        conditions = self.all_conditions()
        logging.debug('CONDITIONS: %s', conditions)

        return


    def process_part(self, part, wf=None, condpath=[]):

        if wf is None:
            wf = self.workflows['in']

        logging.debug('-- WORKFLOW: %s', wf)
        logging.debug('PART: %s', part)

        inst_list = wf.strip('{}').split(',')
        for inst in inst_list:

            logging.debug('INST: %s', inst)

            if ':' in inst:
                cond, action = inst.split(':')
                logging.debug('C/A: %s / %s', cond, action)

                if '>' in cond:
                    key, val = cond.split('>')
                    met_cond = True if part[key] > int(val) else False
                if '<' in cond:
                    key, val = cond.split('<')
                    met_cond = True if part[key] < int(val) else False
            else:
                action = inst
                met_cond = True

            if met_cond is True:
                if action == 'R':
                    logging.debug('REJECT')
                    return False
                elif action == 'A':
                    logging.debug('ACCEPT')
                    return True
                else:
                    logging.debug('WF[%s]', action)
                    return self.process_part(part, self.workflows[action])


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 19', epilog='https://adventofcode.com')
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

    wf = Workflow(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        parts_total = wf.sum_parts()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', parts_total, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        poss_sum = wf.all_acceptable()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', poss_sum, round(end - start, 4))

