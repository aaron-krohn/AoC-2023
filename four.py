import logging
import argparse

from pathlib import Path


class ScratchOffs:

    def __init__(self, cards_raw):

        self.cards = None

        self.parse_cards(cards_raw)


    def parse_cards(self, raw_data):

        self.cards = []

        lines = raw_data.split('\n')

        for line in lines:

            parts = line.split(': ')

            card_id = int(parts[0].split()[1])
            nums_raw = parts[1].split(' | ')

            winning = nums_raw[0].split()
            mynums = nums_raw[1].split()

            self.cards.append({
                    'win': winning,
                    'my': mynums,
                    })


    def sum_points(self):

        total = 0

        for cid, card in enumerate(self.cards):

            points = 0

            for win in card['win']:

                if win in card['my']:
                    if points == 0:
                        points = 1
                    else:
                        points = points * 2

            total += points

        return total


    def count_wins(self, card_id):

        winners = 0
        for win in self.cards[card_id]['win']:
            if win in self.cards[card_id]['my']:
                winners += 1

        return winners


    def total_cards(self, card_id):

        logging.debug('CARD_ID: %s', card_id)

        winners = self.count_wins(card_id)
        #logging.debug('WINNERS: %s', winners)

        if not winners:
            return 0

        subwins = 0
        for offset in range(1, winners+1):
            #logging.debug('%s -> SUB: %s', card_id, card_id+offset)
            subwins += self.total_cards(card_id+offset)

        return winners + subwins


    def all_card_totals(self):

        total = len(self.cards)

        for i in range(len(self.cards)):

            tcards = self.total_cards(i)
            total += self.total_cards(i)

        return total


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 4', epilog='https://adventofcode.com')
    parser.add_argument('-d', '--debug', dest='debug', action='store_true', default=False, help='Show debug output')
    parser.add_argument('-p1', '--part-1', dest='p1', action='store_true', default=False, help='Only run part 1')
    parser.add_argument('-p2', '--part-2', dest='p2', action='store_true', default=False, help='Only run part 2, overrides -p1')

    parsed = parser.parse_args()

    return parsed


if __name__ == '__main__':

    conf = parse_args()

    loglevel = logging.DEBUG if conf.debug else logging.INFO
    logging.basicConfig(level=loglevel, format='%(asctime)s [%(levelname)s] %(message)s')

    datafile = '.'.join([Path(__file__).stem, 'input'])

    with open(datafile, 'r') as f:
        data_in = f.read().strip()

    scratchers = ScratchOffs(data_in)

    ##
    # Part 1
    if not conf.p2:
        card_points = scratchers.sum_points()
        logging.info('[Part 1] Total Points: %s', card_points)

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        total_cards = scratchers.all_card_totals()
        #total_cards = scratchers.total_cards(0)
        #total_cards = scratchers.count_wins(0)
        logging.info('[Part 2] Total Cards: %s', total_cards)

