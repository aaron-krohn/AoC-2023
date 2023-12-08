import math
import logging
import argparse

from pathlib import Path

def parse_map(raw_data):

    node_data = {}
    turns, nodes_raw = raw_data.split('\n\n')

    for node_raw in nodes_raw.split('\n'):

        node, dirs = node_raw.split(' = ')
        left, right = dirs.strip('()').split(', ')
        node_data[node] = (left, right)

    return turns, node_data


def follow_map(turns, nodes, start='AAA', end='ZZZ'):

    logging.debug('TURNS: %s', turns)

    tidx = 0
    total_turns = 0
    nturns = len(turns)
    key = start

    while not key.endswith(end):
        logging.debug('KEY: %s', key)
        logging.debug('NODE: %s', nodes[key])

        ti = tidx % nturns
        t = 0 if turns[ti] == 'L' else 1

        logging.debug('T: %s', t)

        key = nodes[key][t]

        tidx += 1
        total_turns += 1

    return total_turns


def quantum_follow(turns, nodes):

    keys = []

    for key in nodes:
        if key[-1] == 'A':
            keys.append(key)

    total_turns = []

    for key in keys:
        num_turns = follow_map(turns, nodes, start=key, end='Z')
        total_turns.append(num_turns)

    return math.lcm(*total_turns)


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 6', epilog='https://adventofcode.com')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Show debug output')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use test input file')
    parser.add_argument('-p1', '--part-1', dest='p1', action='store_true', default=False, help='Only run part 1')
    parser.add_argument('-p2', '--part-2', dest='p2', action='store_true', default=False, help='Only run part 2, overrides -p1')

    parsed = parser.parse_args()

    return parsed


if __name__ == '__main__':

    conf = parse_args()

    loglevel = logging.DEBUG if conf.debug else logging.INFO
    logging.basicConfig(level=loglevel, format='%(asctime)s [%(levelname)s] %(message)s')

    fn = [Path(__file__).stem, 'input']
    if conf.test:
        fn.insert(1, 'test')
    datafile = '.'.join(fn)

    with open(datafile, 'r') as f:
        data_in = f.read().strip()

    turns, nodes = parse_map(data_in)

    ##
    # Part 1
    if not conf.p2:
        num_turns = follow_map(turns, nodes)
        logging.info('[Part 1] Solution: %s', num_turns)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        num_turns = quantum_follow(turns, nodes)
        logging.info('[Part 2] Solution: %s', num_turns)

