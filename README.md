# Advent of Code 2023

My solutions to AoC 2023.

## Usage

Input files are automatically loaded. Save with same filename as the script, but change extension to `.input`. For example, `five.py` will load `five.input`.

And if you want to run the script using the much shorter test data provided in the problem description, save it to `five.test.input`, and pass the `--test` flag.

To enable debug logging output, use `-d` or `--debug` flag. Otherwise, log level is `logging.INFO`.

Run only one test by passing the `-p1`/`--part-1` or `-p2`/`--part-2` flags. 

```
$ python3.11 five.py --help
usage: five.py [-h] [-d] [-t] [-p1] [-p2]

2023 Advent of Code, Day _

options:
  -h, --help     show this help message and exit
  -d, --debug    Show debug output
  -t, --test     Use test input file
  -p1, --part-1  Only run part 1
  -p2, --part-2  Only run part 2, overrides -p1

https://adventofcode.com
```

## Scores

```
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
  5   01:56:58   12980      0   15:26:51   30073      0
  4   00:12:43    4492      0   01:45:46   13415      0
  3   23:36:21   78639      0   23:42:38   67343      0
  2       >24h  118836      0       >24h  114524      0
  1       >24h  174004      0       >24h  147852      0
```
