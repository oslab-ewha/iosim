# iosim (block I/O simulator)

- This tool aims to prove our preliminary idea about ML storage

## Running Environment

- python3, scikit-learn required

## Usage
```
Usage: iosim.py [<options>] <path>
  <options>
   -h: help(this message)
   -c <size in blks>
   -t <storage type>: all, default(no prefetch, lru), prefetch, ml, rule
   -i <interval>
   -d <bmp dim>
   -L <lba max>
   -m <model path>: for storage ml only
   -M <model type>: for storage ml only
```
