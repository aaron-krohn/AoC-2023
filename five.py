import logging
import argparse

from pathlib import Path

class Almanac:

    def __init__(self, raw_data):

        self.maps = {}
        self.seeds = []
        self.resources = []

        self.parse_almanac(raw_data)


    def parse_almanac(self, raw_data):

        for section in raw_data.split('\n\n'):

            lines = section.split('\n')
            parts = lines[0].split(':')

            if parts[0] == 'seeds':
                self.seeds = [int(x) for x in parts[1].strip().split()]
                continue

            map_name = parts[0].split()[0]
            self.maps.setdefault(map_name, [])

            self.load_map(map_name, lines[1:])


    def load_map(self, map_name, lines):

        nparts = map_name.split('-')

        if nparts[0] not in self.resources:
            self.resources.append(nparts[0])

        if nparts[-1] not in self.resources:
            self.resources.append(nparts[-1])

        for line in lines:

            dest, src, ranj = [int(x) for x in line.split()]

            mapping = {'src': src, 'dest': dest, 'range': ranj}
            self.maps[map_name].append(mapping)


    def find_seed_path(self, seed):

        seed_path = {}
        key = seed

        for i in range(len(self.resources) - 1):

            seed_path.setdefault(self.resources[i], key)
            map_name = '-'.join([self.resources[i], 'to', self.resources[i+1]])

            val = self.map_lookup(map_name, key)
            key = val

        seed_path.setdefault(self.resources[i+1], val)
        return seed_path


    def map_lookup(self, map_name, key):
        ##
        # seed-to-soil map:
        # 50 98 2
        # 52 50 48

        val = None
        for mapping in self.maps[map_name]:
            if key >= mapping['src'] and key <= mapping['src'] + mapping['range']:
                val = (key - mapping['src']) + mapping['dest']
                break

        if val is None:
            return key

        return val


    def find_nearest_location(self, seed_ranges=False):

        nearest = None

        if not seed_ranges:

            for seed in self.seeds:

                seed_path = self.find_seed_path(seed=seed)
                if nearest is None or seed_path['location'] < nearest['location']:
                    nearest = seed_path

        else:

            for ss_idx in range(0, len(self.seeds), 2):

                seed_start = self.seeds[ss_idx]
                seed_end = seed_start + self.seeds[ss_idx+1]

                logging.info('SEEDS: %s -> %s', seed_start, seed_end)

                for seed in range(seed_start, seed_end + 1):

                    seed_path = self.find_seed_path(seed=seed)
                    if nearest is None or seed_path['location'] < nearest['location']:
                        nearest = seed_path

        return nearest


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 5', epilog='https://adventofcode.com')
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

    almanac = Almanac(data_in)

    ##
    # Part 1
    if not conf.p2:
        min_location = almanac.find_nearest_location()
        logging.info('[Part 1] Min Location: %s', min_location)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        min_location = almanac.find_nearest_location(seed_ranges=True)
        logging.info('[Part 2] Min Location: %s', min_location)

