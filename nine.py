import time
import logging
import argparse

from pathlib import Path


def parse_readings(raw_data):

    readings = []

    for line in raw_data.split('\n'):

        reading = [int(x) for x in line.split()]
        readings.append(reading)

    return readings


def diff_list(reading):

    diffs = []

    for idx in range(len(reading) - 1):

        logging.debug('%s - %s', reading[idx+1], reading[idx])
        diffs.append(reading[idx+1] - reading[idx])

    logging.debug('DIFFS: %s', diffs)
    return diffs


def predict_reading(reading):

    diff_history = []
    diff_history.append(reading[-1])

    diffs = diff_list(reading)
    diff_history.append(diffs[-1])

    while any(diffs):

        diffs = diff_list(diffs)
        diff_history.append(diffs[-1])

    prediction = sum(diff_history)
    logging.debug('PREDICTED: %s = SUM(%s)', prediction, diff_history)

    return prediction


def extrapolate_history(readings):

    total_extra = 0

    for reading in readings:
        diff_history = [reading]

        logging.debug('READING: %s', reading)
        diff = diff_list(reading)

        while any(diff):
            diff_history.append(diff)
            diff = diff_list(diff)
        diff_history.append(diff)


        logging.debug('HISTORY: %s', diff_history)

        f = 0
        for didx in range(len(diff_history) - 1, 0, -1):

            logging.debug('DIDX: %s', didx)
            logging.debug('%s - %s', diff_history[didx-1][0], f)
            f = diff_history[didx-1][0] - f
            logging.debug('= %s', f)

        total_extra += f

    return total_extra


def sum_predictions(readings):

    predictions = []

    for reading in readings:
        logging.debug('READINGS: %s', reading)
        prediction = predict_reading(reading)
        predictions.append(prediction)

    sum_pred = sum(predictions)
    logging.debug('PREDICTIONS: %s = SUM(%s)', sum_pred, predictions)
    return sum_pred


def parse_args():

    parser = argparse.ArgumentParser(description='2023 Advent of Code, Day 9', epilog='https://adventofcode.com')
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

    readings = parse_readings(data_in)

    ##
    # Part 1
    if not conf.p2:
        start = time.time()
        predictions_total = sum_predictions(readings)
        end = time.time()
        logging.info('[Part 1] Solution: %s in %s seconds', predictions_total, round(end - start, 4))

    ##
    # Part 2
    if not conf.p1 or conf.p2:
        start = time.time()
        predictions_total = extrapolate_history(readings)
        end = time.time()
        logging.info('[Part 2] Solution: %s in %s seconds', predictions_total, round(end - start, 4))

