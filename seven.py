import time
import logging
import argparse

from functools import cmp_to_key

from pathlib import Path


class CamelPoker:

    def __init__(self, raw_data, jokers=False):

        self.hands = self.parse_hands(raw_data)
        self.jokers = jokers


    def parse_hands(self, raw_data):

        hands = {}

        for line in raw_data.split('\n'):

            hand, bid = line.split()
            hands.setdefault(hand, int(bid))

        return hands


    def simulate(self):

        total_score = 0

        all_hands = list(self.hands.keys())
        all_hands.sort(key=cmp_to_key(self.hand_cmp))

        for rank, hand in enumerate(all_hands):

            logging.debug('HAND: %s / RANK %s / BID %s', hand, (rank + 1), self.hands[hand])
            total_score += self.hands[hand] * (rank + 1)

        logging.debug('NUM HANDS: %s', len(all_hands))
        return total_score


    def hand_cmp(self, hand_one, hand_two):

        rank_one = self.rank_hand(hand_one)
        rank_two = self.rank_hand(hand_two)

        logging.debug('HAND 1: %s (%s) / HAND 2: %s (%s)', hand_one, rank_one, hand_two, rank_two)

        if rank_one == rank_two:
            breaker = self.tie_breaker(hand_one, hand_two)
            return breaker

        if rank_one > rank_two:
            logging.debug('%s > %s', rank_one, rank_two)
            return 1

        if rank_one < rank_two:
            logging.debug('%s < %s', rank_one, rank_two)
            return -1

        logging.debug('TIED! %s == %s', rank_one, rank_two)
        return 0


    def rank_hand(self, hand):

        counts = self.of_each(hand)

        if self.is_five_kind(counts):
            return 6

        if self.is_four_kind(counts):
            return 5

        if self.is_full_house(counts):
            return 4

        if self.is_three_kind(counts):
            return 3

        if self.is_two_pair(counts):
            return 2

        if self.is_one_pair(counts):
            return 1

        return 0


    def tie_breaker(self, hand_one, hand_two):

        if self.jokers:
            cards = 'J23456789TQKA'
        else:
            cards = '23456789TJQKA'

        for idx in range(0, len(hand_one)):

            if cards.index(hand_one[idx]) > cards.index(hand_two[idx]):
                logging.debug('TB: %s (%s) > %s (%s)', hand_one[idx], cards.index(hand_one[idx]), hand_two[idx], cards.index(hand_two[idx]))
                return 1

            if cards.index(hand_one[idx]) < cards.index(hand_two[idx]):
                logging.debug('TB: %s (%s) < %s (%s)', hand_one[idx], cards.index(hand_one[idx]), hand_two[idx], cards.index(hand_two[idx]))
                return -1

        logging.debug('TB: TIED')
        return 0


    def of_each(self, hand):

        counts = {}
        for char in hand:
            counts.setdefault(char, 0)
            counts[char] += 1

        if self.jokers and 'J' in counts:

            logging.debug('JACKS: %s', counts)

            num_jokers = counts['J']
            if num_jokers == 5:
                return counts

            del counts['J']

            max_key = None
            for key, val in counts.items():
                if max_key is None:
                    max_key = key
                if val > counts[max_key]:
                    max_key = key

            counts[max_key] += num_jokers
            logging.debug('JOKERS: %s', counts)

        return counts


    def is_five_kind(self, counts):

        if 5 in counts.values():
            return True

        return False


    def is_four_kind(self, counts):

        if 4 in counts.values():
            return True

        return False


    def is_full_house(self, counts):

        if 3 in counts.values() and 2 in counts.values():
            return True

        return False


    def is_three_kind(self, counts):

        if 3 in counts.values():
            return True

        return False


    def is_two_pair(self, counts):

        num_twos = 0
        for c in counts.values():
            if c == 2:
                num_twos += 1

        if num_twos == 2:
            return True

        return False


    def is_one_pair(self, counts):

        if 2 in counts.values():
            return True

        return False


    def is_high_card(self, counts):

        num_ones = 0
        for c in counts.values():
            if c == 1:
                num_ones += 1

        if num_ones == 5:
            return True

        return False


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 7', epilog='https://adventofcode.com')
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

    cp = CamelPoker(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        score = cp.simulate()
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', score, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        cp.jokers = True
        start = time.time()
        score = cp.simulate()
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', score, round(end - start, 4))

