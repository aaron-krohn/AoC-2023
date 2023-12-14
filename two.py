import time
import logging
import argparse

from pathlib import Path


def parse_game(game_str):

    logging.debug('GAMESTR: %s', game_str)

    gdata = {}

    parts = game_str.split(': ')
    gid = int(parts[0].split()[1])

    gdata.setdefault(gid, [])

    pulls = parts[1].split('; ')

    for pull in pulls:
        color_counts = pull.split(', ')
        pdata = {}
        for count in color_counts:
            praw = count.split()
            amt = int(praw[0])
            color = praw[1]
            pdata[color] = amt
        gdata[gid].append(pdata)

    return gdata


def sum_possible(games, red=None, green=None, blue=None):

    psum = 0

    for gid, gdata in games.items():
        logging.debug('Game: %s', gid)

        possible = True

        for pull in gdata:

            logging.debug('PULL: %s', pull)

            if red is not None and pull.setdefault('red', 0) > red:
                possible = False
                break

            if green is not None and pull.setdefault('green', 0) > green:
                possible = False
                break

            if blue is not None and pull.setdefault('blue', 0) > blue:
                possible = False
                break

        if possible:
            logging.debug('PSUM ADDING: %s', gid)
            psum += gid

    return psum


def sum_min_power(games):

    gp_sum = 0

    for gid, gdata in games.items():

        logging.debug('Game: %s', gid)

        rmin = None
        gmin = None
        bmin = None

        for pull in gdata:

            logging.debug('Pull: %s', pull)

            rpull = pull.setdefault('red', -1)
            if rpull > 0 and (rmin is None or rpull > rmin):
                rmin = rpull

            gpull = pull.setdefault('green', -1)
            if gpull > 0 and (gmin is None or gpull > gmin):
                gmin = gpull

            bpull = pull.setdefault('blue', -1)
            if bpull > 0 and (bmin is None or bpull > bmin):
                bmin = bpull

        mult = []
        if rmin is not None:
            mult.append(rmin)
        if gmin is not None:
            mult.append(gmin)
        if bmin is not None:
            mult.append(bmin)

        logging.debug('Mult: %s', mult)

        if not mult:
            continue

        mult_total = 1
        for m in mult:
            mult_total = mult_total * m

        logging.debug('MT: %s', mult_total)

        gp_sum += mult_total

    logging.debug('GP_SUM: %s', gp_sum)
    return gp_sum


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 2', epilog='https://adventofcode.com')
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

    games_raw = data_in.split('\n')
    games = {}
    for game_str in games_raw:
        games.update(parse_game(game_str))

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        psummed = sum_possible(games, red=12, green=13, blue=14)
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', psummed, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        mps = sum_min_power(games)
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', mps, round(end - start, 4))

