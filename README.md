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

On problem 5.2, I wrote really bad code and never got around to making it fast. I'm not even sure how to make it fast, so it took about 11.5 hours to brute force. Shame. Included `five.log` to show just how bad it was.

For problem 8.2, I looked on reddit for a hint. The hint made the solution pretty blatantly obvious, and it's one I doubt I would have ever thought of on my own. I'd still be brute forcing it, probably for days. I feel like I cheated.

Day 9, I decided to sleep like a person instead of staying up late.

Day 10.2 was not great. I tried implementing flood fill, but went back to a boundary counting method. Leaving the flood fill code because of how ridiculous it is.

```
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 11   00:46:13    5844      0   01:56:04    8417      0
 10   02:28:34    8936      0   23:31:28   27543      0
  9   12:31:50   39119      0   19:34:08   46162      0
  8   00:19:49    5725      0   01:25:03    6710      0
  7   01:30:09    9640      0   02:16:55    9312      0
  6   00:20:59    7028      0   00:26:06    6255      0
  5   01:56:58   12980      0   15:26:51   30073      0
  4   00:12:43    4492      0   01:45:46   13415      0
  3   23:36:21   78639      0   23:42:38   67343      0
  2       >24h  118836      0       >24h  114524      0
  1       >24h  174004      0       >24h  147852      0
```
