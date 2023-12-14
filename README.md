# Advent of Code 2023

My solutions to AoC 2023.

## Usage

Input files are automatically loaded. Save with same filename as the script, but change extension to `.input`. For example, `five.py` will load `five.input`.

And if you want to run the script using the much shorter test data provided in the problem description, save it to `five.test.input`, and pass the `--test` flag.

To enable debug logging output, use `-d` or `--debug` flag. Otherwise, log level is `logging.INFO`.

Run only one test by passing the `-p1`/`--part-1` or `-p2`/`--part-2` flags. 

Save log to a file with `-l` or `--log` e.g. `--log ten.log`

```
$ python3.11 ten.py --help
usage: ten.py [-h] [-d] [-t] [-p1] [-p2] [-l LOGFILE]

2023 Advent of Code, Day 10

options:
  -h, --help            show this help message and exit
  -d, --debug           Show debug output
  -t, --test            Use test input file
  -p1, --part-1         Only run part 1
  -p2, --part-2         Only run part 2, overrides -p1
  -l LOGFILE, --log LOGFILE
                        Filename for writing log file

https://adventofcode.com
```

## Scores

```
      --------Part 1---------   --------Part 2---------
Day       Time    Rank  Score       Time    Rank  Score
 14   00:39:15    5515      0   10:24:39   14991      0
 13   00:32:20    2384      0   03:52:00    7925      0
 12   02:02:22    6957      0          -       -      -
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

## Problem Notes

A brief review of why things went wrong. Not so much how they could get better because, let's be honest, these problems are a bit out of my league, and improving these algorithms would take days or weeks of researching how a proper programmer with computer science background would approach things.

### Problem 5.2

I wrote really slow code and never got around to making it fast. I'm not even sure how to make it fast, so it took about 11.5 hours to brute force. Shame. Included `five.log` to show just how bad it was.

### Problem 8.2

I looked on reddit for a hint. The hint made the solution pretty blatantly obvious, and it's one I doubt I would have ever thought of on my own. I'd still be brute forcing it, probably for days. I feel like I cheated.

### Day 9

I decided to sleep like a person instead of staying up late to finish as fast as possible

### Problem 10.2

... not great. I tried implementing flood fill, but went back to a boundary counting method. Leaving the flood fill code because of how ridiculous it is, despite almost working. See code comments for detailed explaination.

### Problem 12.2

This one is... elusive, to say the least.

### Problem 14

Another one of my very slow algorithm. I think my weakness is trying to code the problem in terms of human abstraction and understanding rather than a purely numerical, fast way of doing it. My lack of classical computer science training is revealing my limitations.

I found it very interesting that both the sample dataset, a 10x10 ascii grid, and the problem input, a 100x100 grid, took almost exactly the same amount of time, 2949 seconds and 3036 seconds, respectively, for a billion (1000000000)  cycles. My solution uses `functools.lru_cache` but in order to do so, the data must be hashable, so each cycle converted the data from an array to a string and back. I wonder if this was worth the tradeoff.

I went to bed after starting the final computation, assuming it would take much longer than the test data set, hence the low ranking and long time to completion despite being finished six hours earlier.

## Problem Compute Times

I didn't think to start doing this until day 14, so forgive the timestamps, but I went through and ran them all again, unmodified.

Answer are redacted because of AoC terms of use.

### Day 1

```
$ python3.11 one.py
2023-12-14 14:32:17,734 [INFO] [Part 1] Solution: XXXXX in 0.0616 seconds
2023-12-14 14:32:17,860 [INFO] [Part 2] Solution: XXXXX in 0.1265 seconds
```

### Day 2

```
$ python3.11 two.py
2023-12-14 14:32:22,125 [INFO] [Part 1] Solution: XXXX in 0.0004 seconds
2023-12-14 14:32:22,126 [INFO] [Part 2] Solution: XXXXX in 0.0006 seconds
```

### Day 3

```
$ python3.11 three.py
2023-12-14 14:32:28,019 [INFO] [Part 1] Solution: XXXXXX in 0.0191 seconds
2023-12-14 14:32:28,029 [INFO] [Part 2] Solution: XXXXXXXX in 0.0106 seconds
```

### Day 4

```
$ python3.11 four.py
2023-12-14 14:34:27,251 [INFO] [Part 1] Solution: XXXXX in 0.0009 seconds
2023-12-14 14:36:35,420 [INFO] [Part 2] Solution: XXXXXXXX in 128.1694 seconds
```

### Day 5

```
$ python3.11 five.py
2023-12-14 14:42:23,318 [INFO] [Part 1] Solution: XXXXXXXXX in 0.0004 seconds
```

### Day 6

```
$ python3.11 six.py
2023-12-14 14:45:37,627 [INFO] [Part 1] Solution: XXXXXXX in 0.0002 seconds
2023-12-14 14:45:44,419 [INFO] [Part 2] Solution: XXXXXXXX in 6.7919 seconds
```

### Day 7

```
$ python3.11 seven.py
2023-12-14 14:48:36,074 [INFO] [Part 1] Solution: XXXXXXXXX in 0.0654 seconds
2023-12-14 14:48:36,155 [INFO] [Part 2] Solution: XXXXXXXXX in 0.0805 seconds
```

### Day 8

```
$ python3.11 eight.py
2023-12-14 14:50:42,657 [INFO] [Part 1] Solution: XXXXX in 0.051 seconds
2023-12-14 14:50:42,960 [INFO] [Part 2] Solution: XXXXXXXXXXXXXX in 0.3023 seconds
```

### Day 9

```
$ python3.11 nine.py
2023-12-14 14:52:59,585 [INFO] [Part 1] Solution: XXXXXXXXXX in 0.0255 seconds
2023-12-14 14:52:59,622 [INFO] [Part 2] Solution: XXX in 0.0372 seconds
```

### Day 10

```
$ python3.11 ten.py
2023-12-14 15:01:13,523 [INFO] [Part 1] Solution: XXXX in 0.0707 seconds
2023-12-14 15:03:21,075 [INFO] [Part 2] Solution: XXX in 127.5522 seconds
```

### Day 11

```
$ python3.11 eleven.py
2023-12-14 15:04:09,932 [INFO] [Part 1] Solution: XXXXXXXX in 1.1103 seconds
2023-12-14 15:04:11,054 [INFO] [Part 2] Solution: XXXXXXXXXXXX in 1.1215 seconds
```

### Day 12
```
$ python3.11 twelve.py --part-1
2023-12-14 15:08:28,598 [INFO] [Part 1] Solution: XXXXX in 2.3818 seconds
```

### Day 13
```
$ python3.11 thirteen.py 
2023-12-14 15:11:06,791 [INFO] [Part 1] Solution: XXXXX in 0.0014 seconds
2023-12-14 15:11:06,816 [INFO] [Part 2] Solution: XXXXX in 0.0246 seconds
```

### Day 14

```
$ python3.11 fourteen.py
2023-12-14 15:13:19,149 [INFO] [Part 1] Solution: XXXXXX in 0.0083 seconds
2023-12-14 04:15:33,964 [INFO] [Part 2] Solution: XXXXX in 3035.9854 seconds
```
