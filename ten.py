import logging
import argparse

from pathlib import Path


class PipeMap:

    def __init__(self, raw_data):

        self.map = []
        self.start = None
        self.pos = None
        self.s = None

        self.parse_map(raw_data)
        self.find_start()

        self.route = []
        self.inner = []
        self.outer = []


    def parse_map(self, raw_data):

        rows = raw_data.split('\n')
        self.map = rows


    def find_start(self):

        for ridx, row in enumerate(self.map):

            for cidx, col in enumerate(row):

                if col == 'S':

                    logging.debug('START: %s', (ridx, cidx))
                    self.start = (ridx, cidx)
                    self.pos = (ridx, cidx)


    def get_neighbors(self, ridx, cidx):
        """Determine the pair of neighboring coordinates for a
           given tile in the pipe route
        """

        lookup = {
                '|': ((ridx-1, cidx), (ridx+1, cidx)),
                '-': ((ridx, cidx-1), (ridx, cidx+1)),
                'F': ((ridx+1, cidx), (ridx, cidx+1)),
                '7': ((ridx+1, cidx), (ridx, cidx-1)),
                'J': ((ridx-1, cidx), (ridx, cidx-1)),
                'L': ((ridx-1, cidx), (ridx, cidx+1))
                }

        # Because, why not
        if (ridx, cidx) == self.start:
            neigh = []
            if self.map[ridx-1][cidx] in ['|', 'F', '7']:
                neigh.append((ridx-1, cidx))
            if self.map[ridx+1][cidx] in ['|', 'J', 'L']:
                neigh.append((ridx+1, cidx))
            if self.map[ridx][cidx-1] in ['-', 'F', 'L']:
                neigh.append((ridx, cidx-1))
            if self.map[ridx][cidx+1] in ['-', '7', 'J']:
                neigh.append((ridx, cidx+1))

        else:
            neigh = lookup[self.map[ridx][cidx]]

        logging.debug('NEIGH: %s', neigh)
        return neigh


    def s_tile(self):
        """If 'S' were a tile, which tile would it be? -__-
           Use neighboring tiles to infer. Even this is needlessly difficult.
        """

        neighs = self.get_neighbors(*self.start)
        logging.debug('NEIGHS: %s', neighs)

        above, below, left, right = False, False, False, False

        # Determine whether each of the neighbor coords is above/below/left or right
        for coords in neighs:

            ridx, cidx = coords

            if self.start[0] - ridx == 0:
                if self.start[1] - cidx < 0:
                    right = True
                elif self.start[1] - cidx > 0:
                    left = True

            if self.start[1] - cidx == 0:
                if self.start[0] - ridx < 0:
                    below = True
                elif self.start[0] - ridx > 0:
                    above = True

        logging.debug('ABOVE / BELOW / LEFT / RIGHT: %s / %s / %s / %s', above, below, left, right)

        # Use relative neighbor locations to determine tile type
        if above and below:
            return '|'
        if above and right:
            return 'L'
        if above and left:
            return 'J'
        if below and right:
            return 'F'
        if below and left:
            return '7'
        if left and right:
            return '-'


    def trace_route(self):
        """Starting at tile 'S', follow the path until we reach 'S' again
        """

        if not self.start:
            self.find_start()

        if self.route:
            self.route = []

        # Remember where we just were so we don't go backwards and infinite loop
        # ourself. That totally didn't happen, I swear.
        backward = self.start
        neigh = self.get_neighbors(*self.pos)
        self.route.append(neigh[0])
        self.move(*neigh[0])
        logging.debug('POS: %s', self.pos)

        while self.map[self.pos[0]][self.pos[1]] != 'S':

            neigh = self.get_neighbors(*self.pos)
            logging.debug('NEIGH: %s / ROUTE: %s', neigh, self.route[-1])

            # Don't use the neighbor we were just at
            if neigh[0] == backward:
                n = 1
            else:
                n = 0
            logging.debug('N: %s', n)

            self.route.append(neigh[n])
            backward = self.pos
            self.move(*neigh[n])

            logging.debug('POS: %s', self.pos)


    def move(self, ridx, cidx):

        self.pos = (ridx, cidx)


    def furthest_step(self):
        """Solution to part 1: find the distance of the furthest tile in the route
        """

        if not self.route:
            self.trace_route()

        return len(self.route) / 2


    def outer_fill(self, ridx=0, cidx=0):
        """This was almost, so close to working. The dilemma I eventually ran into was this:
           The rules said that travel between adjacent pipes was legal so long as no boundary
           is crossed. Meaning, you can have a completely enclosed tile that is still outside
           the loop, technically.

           While this makes sense, it really complicates things for the flood fill method
           attempted here. After reading some reddit comments, it looks like some folks simply
           doubled the size of the map. I wasn't that smart.

           To solve the squeeze problem, I attempted to treat the pipe as also "outside" even
           though it was a boundary. This was great right up to the edge case where, for
           example, an 'L' tile, when approached from above-right, is a boundary to the area
           below-left. But if you approach from below-left, it is a boundary to above-right.

           Obviously, the same time can't simultaneously be a boundary for multiple coordinates.
           So I gave up and went back to counting boundary crossings.
        """

        if not self.route:
            self.trace_route()

        if (ridx, cidx) in self.route:
            logging.error('Invalid starting coords: %s', (ridx,cidx))
            return

        self.outer.append((ridx,cidx))

        idx = -1
        while idx < len(self.outer) - 1:
            idx += 1
            coords = self.outer[idx]
            tile = self.map[coords[0]][coords[1]]
            logging.debug('COORDS: %s [%s]', coords, tile)

            # What the fuck

            # Above
            if not (coords[0] - 1 < 0 or (coords in self.route and tile in ['-','7','F'])):
                testco = (coords[0]-1,coords[1])
                logging.debug('OUTER: Above %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0]-1,coords[1]))
            # Above-Left
            if not (coords[0] - 1 < 0 or coords[1] - 1 < 0 or (coords in self.route and tile in ['-','|','J','7','F'])):
                testco = (coords[0]-1,coords[1]-1)
                logging.debug('OUTER: Above-Left %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0]-1,coords[1]-1))
            # Above-Right
            if not (coords[0] - 1 < 0 or coords[1] + 1 >= len(self.map[coords[0]-1]) or (coords in self.route and tile in ['-','|','J','7','F','L'])):
                testco = (coords[0]-1,coords[1]+1)
                logging.debug('OUTER: Above-Right %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0]-1,coords[1]+1))
            # Right
            if not (coords[1] + 1 >= len(self.map[coords[0]]) or (coords in self.route and tile in ['|','7','J'])):
                testco = (coords[0],coords[1]+1)
                logging.debug('OUTER: Right %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0],coords[1]+1))
            # Left
            if not (coords[1] - 1 < 0 or (coords in self.route and tile in ['|','L','F'])):
                testco = (coords[0],coords[1]-1)
                logging.debug('OUTER: Left %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0],coords[1]-1))
            # Below
            if not (coords[0] + 1 >= len(self.map) or (coords in self.route and tile in ['-','J','L'])):
                testco = (coords[0]+1,coords[1])
                logging.debug('OUTER: Below %s', testco)
                if testco not in self.outer:
                    self.outer.append(testco)
            # Below-Left
            if not (coords[0] + 1 >= len(self.map) or coords[1] - 1 < 0 or (coords in self.route and tile in ['-','|','L','J'])):
                testco = (coords[0]+1,coords[1]-1)
                logging.debug('OUTER: Below-Left %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0]+1,coords[1]-1))
            # Below-Right
            if not (coords[0] + 1 >= len(self.map) or coords[1] + 1 >= len(self.map[coords[0]]) or (coords in self.route and tile in ['-','|','L','J'])):
                testco = (coords[0]+1,coords[1]-1)
                logging.debug('OUTER: Below-Right %s', testco)
                if testco not in self.outer:
                    self.outer.append((coords[0]+1,coords[1]+1))

        self.inner = []
        for rix, row in enumerate(self.map):
            for cix, tile in enumerate(row):
                if (rix,cix) not in self.route and (rix,cix) not in self.outer:
                    self.inner.append((rix,cix))

        logging.debug('INNER: %s', self.inner)


    def is_enclosed(self, ridx, cidx):
        '''How many boundaries does a laser beam from the left cross before getting
           to the target tile?

           A 'U'-shaped boundary isn't a boundary because you never cross into the
           inner part of the loop: LJ or F7

           But you do when it's a chicane shape: L7 or FJ. And obviously | counts, too.

           Except when the tile isn't part of the pipe route, then it's just a piece
           of the ground and we ignore it.

           If we cross an odd-number of boundaries, we're inside the loop.
        '''

        logging.debug('RIDX,CIDX: %s,%s', ridx, cidx)

        if (ridx,cidx) in self.route:
            logging.debug('IN ROUTE')
            return False

        bounds = 0
        f_open, l_open = False, False
        for cix, tile in enumerate(self.map[ridx]):

            # I'm sure there's a better way, but I'm so over this.

            if cix == cidx:
                logging.debug('CIX (%s) == CIDX (%s)', cix, cidx)
                break

            if (ridx, cix) not in self.route:
                continue

            logging.debug('TILE: %s', tile)

            if tile == 'S':
                tile = self.s_tile()

            if tile == 'F':
                logging.debug('OPEN_F')
                f_open = True
            if tile == 'L':
                logging.debug('OPEN_L')
                l_open = True

            if tile in ['|','F','7','J','L']:
                logging.debug('BOUNDS++')
                bounds += 1

            if tile == '7' and f_open:
                logging.debug('CLOSE_F, BOUNDS - 2')
                bounds -= 2
                f_open = False
            if tile == 'J' and l_open:
                logging.debug('CLOSE_L, BOUNDS - 2')
                bounds -= 2
                l_open = False
            if tile == '7' and l_open:
                logging.debug('CLOSE_L, BOUNDS - 1')
                bounds -= 1
                l_open = False
            if tile == 'J' and f_open:
                logging.debug('CLOSE_F, BOUNDS - 1')
                bounds -= 1
                f_open = False

        logging.debug('%s %% 2 == %s', bounds, (bounds%2))
        if bounds % 2 == 1:
            logging.debug('ENCLOSED')
            return True

        logging.debug('NOT ENCLOSED')
        return False


    def count_enclosed(self):
        '''Iterate all tiles and see if they're enclosed
        '''

        if not self.route:
            self.trace_route()

        total_enc = 0

        for ridx, row in enumerate(self.map):
            for cidx, tile in enumerate(row):

                if self.is_enclosed(ridx, cidx):
                    self.inner.append((ridx,cidx))
                    logging.debug('ENCLOSED: (%s,%s)', ridx, cidx)
                    total_enc += 1
                elif (ridx,cidx) not in self.route:
                    self.outer.append((ridx, cidx))

        logging.debug('INNER: %s', self.inner)
        logging.debug('OUTER: %s', self.outer)
        return total_enc


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

    pipes = PipeMap(data_in)


    ##
    # Part 1
    if not conf.p2:
        step_count = pipes.furthest_step()
        logging.info('[Part 1] Solution: %s', step_count)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        total_enc = pipes.count_enclosed()
        logging.info('[Part 2] Solution: %s', total_enc)

