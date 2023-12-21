import math
import time
import logging
import argparse

from pathlib import Path


class CoolestPath:

    def __init__(self, raw_data):

        self.map = self.parse_data(raw_data)

        self.ctlmap = {
                'N': {
                    'left': (0, -1, 'W'),
                    'right': (0, 1, 'E'),
                    'straight': (-1, 0, 'N'),
                    },
                'S': {
                    'left': (0, 1, 'E'),
                    'right': (0, -1, 'W'),
                    'straight': (1, 0, 'S'),
                    },
                'E': {
                    'left': (-1, 0, 'N'),
                    'right': (1, 0, 'S'),
                    'straight': (0, 1, 'E'),
                    },
                'W': {
                    'left': (1, 0, 'S'),
                    'right': (-1, 0, 'N'),
                    'straight': (0, -1, 'W'),
                    },
                }


    def parse_data(self, raw_data):

        return [[int(x) for x in row] for row in raw_data.split('\n')]


    def dijk_ultra(self, ridx=0, cidx=0, heading='east'):
        """Modified version of Djikstra to comply with travel rules:
            - Cannot go backwards
            - Cannot go straight more than 10 times
            - Cannot turn without going straight 4 times
        """

        current = (ridx, cidx, 'E', 1)
        start = current
        finish = (len(self.map)-1, len(self.map[0])-1)

        unvisited = {}

        for rid, row in enumerate(self.map):
            for cid, val in enumerate(row):
                for heading in ['N','E','S','W']:
                    for straits in (1,2,3,4,5,6,7,8,9,10):

                        addr = (rid, cid, heading, straits)
                        unvisited[addr] = 0 if addr == start else math.inf

        heading = current[2]
        straits = current[3]

        final_dist = math.inf

        while True:

            cdist = unvisited[current]
            logging.debug('--- %s: %s', current, cdist)

            if finish == (current[0], current[1]) and cdist < final_dist:
                final_dist = cdist
                final_key = current

            for turn in self.ctlmap[heading]:

                nroff, ncoff, nhead = self.ctlmap[heading][turn]
                logging.debug(' - %s:', turn)
                logging.debug('CTL[%s][%s] -> %s', heading, turn, self.ctlmap[heading][turn])

                nrid = nroff + ridx
                ncid = ncoff + cidx

                if straits == 10 and turn == 'straight':
                    logging.debug('NO STRAIGHT ON 10')
                    continue

                if straits < 4 and turn != 'straight':
                    logging.debug('NO TURN BEFORE 4: %s @ %s', turn, straits)
                    continue

                nstr = straits + 1 if heading == nhead else 1

                addr = (nrid, ncid, nhead, nstr)

                if finish == (nrid, ncid) and nstr < 4:
                    logging.debug('NO FINISH BEFORE 4: %s @ %s', turn, straits)
                    continue

                if addr not in unvisited:
                    logging.debug('ADDR NOT FOUND: %s', addr)
                    continue

                ndist = cdist + self.map[nrid][ncid]
                logging.debug('NDIST: %s', ndist)

                if unvisited[addr] > ndist:
                    unvisited[addr] = ndist

            del unvisited[current]
            logging.debug('VISITED: %s', current)

            if not unvisited:
                break

            next_addr = min(unvisited, key=unvisited.get)
            if unvisited[next_addr] == math.inf:
                logging.debug('NO PATH')
                break

            current = next_addr
            ridx, cidx, heading, straits = current

        logging.debug('FINAL: %s', final_key)
        return final_dist


    def mod_dijkstra(self, ridx, cidx, heading='east'):
        """Modified version of Djikstra to comply with travel rules:
            - Cannot go "backwards"
            - Cannot go straight more than 3 times
        """

        current = (ridx,cidx,'E',3)
        start = current
        finish = (len(self.map)-1, len(self.map[0])-1)

        meta = {}
        visited = {}
        unvisited = {}

        for rid, row in enumerate(self.map):
            for cid, val in enumerate(row):
                for heading in ['N','S','E','W']:
                    for straits in (3,2,1):

                        addr = (rid,cid,heading,straits)
                        unvisited[addr] = 0 if addr == start else math.inf

        meta[start] = (start,)

        while True:

            logging.debug('--- CUR[%s]: %s ---', current, unvisited[current])
            cdist = unvisited[current]
            cpath = meta[current]

            logging.debug('HSP: %s / %s / %s', heading, straits, cpath)

            for turn in self.ctlmap[heading]:

                logging.debug('- TURN: %s', turn)

                nroff, ncoff, nhead = self.ctlmap[heading][turn]

                logging.debug('CTL[%s][%s]: %s / %s / %s', heading, turn, nroff, ncoff, nhead)

                nrid = nroff + ridx
                ncid = ncoff + cidx
                nstr = straits - 1 if heading == nhead else 3

                if nstr == 0:
                    logging.debug('STRAITS = 0')
                    continue

                addr = (nrid,ncid,nhead,nstr)
                logging.debug('ADDR: %s', addr)
                if addr not in unvisited:
                    continue

                logging.debug('DIST - UNVISIT[%s]: %s', addr, unvisited[addr])
                ndist = cdist + self.map[nrid][ncid]
                logging.debug('NDIST: %s', ndist)

                if unvisited[addr] > ndist:
                    npath = list(cpath)
                    npath.append(addr)
                    npath = tuple(npath)

                    unvisited[addr] = ndist

                    meta[addr] = npath
                    logging.debug('META[%s]: %s', addr, meta[addr])

            visited[current] = cdist
            logging.debug('VISITED[%s] = %s', current, cdist)
            del unvisited[current]

            if not unvisited:
                break

            next_addr = min(unvisited, key=unvisited.get)
            if unvisited[next_addr] == math.inf:
                break

            current = next_addr
            ridx, cidx, heading, straits = current

        mins = []
        for key in visited:
            if key[0] == finish[0] and key[1] == finish[1]:
                mins.append(visited[key])
                logging.debug('VISITED[FINISH]: %s', visited[key])

        return min(mins)


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 17', epilog='https://adventofcode.com')
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

    cp = CoolestPath(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        lowest_heat = cp.mod_dijkstra(0, 0)
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', lowest_heat, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        lowest_heat = cp.dijk_ultra()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', lowest_heat, round(end - start, 4))

