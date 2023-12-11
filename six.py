import logging
import argparse

from pathlib import Path


def parse_races(raw_data):

    lines = raw_data.split('\n')

    for line in lines:

        parts = line.split(':')

        if parts[0] == 'Time':
            times = map(int, parts[1].strip().split())

        if parts[0] == 'Distance':
            distances = map(int, parts[1].strip().split())

    return list(zip(list(times), list(distances)))


def calculate_race(race_time, distance):

    win_ways = 0

    for hold_ms in range(1, race_time):

        race_dist = (race_time - hold_ms) * hold_ms

        if race_dist > distance:
            win_ways += 1

    return win_ways


def sim_races(race_data):

    win_counts = []

    for race_time, dist in race_data:

        win_counts.append(calculate_race(race_time, dist))

    logging.info('Win Counts: %s', win_counts)

    mult_total = win_counts[0]
    for i in range(1, len(win_counts)):
        mult_total = mult_total * win_counts[i]

    return mult_total


def run_race(race_data):

    race_time = int(''.join([str(x[0]) for x in race_data]))
    race_dist = int(''.join([str(x[1]) for x in race_data]))

    logging.debug('Race Time/Dist: %s/%s', race_time, race_dist)

    ways = calculate_race(race_time, race_dist)
    return ways


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 6', epilog='https://adventofcode.com')
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

    race_data = parse_races(data_in)

    logging.debug('Race data: %s', race_data)

    ##
    # Part 1
    if not conf.p2:
        races_total = sim_races(race_data)
        logging.info('[Part 1] Solution: %s', races_total)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        race_ways = run_race(race_data)
        logging.info('[Part 2] Solution: %s', race_ways)

