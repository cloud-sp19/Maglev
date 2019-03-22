## Omnet implementation

### To build
1. Make sure that you set env (`. setenv`) from the omnet source.
2. From this directory,
```bash
opp_makemake --deep -f -o run_maglev
```
### To run
1. 
```bash
./run_maglev
```
2. Choose a backend number, e.g. 3.
3. Choose a "large" prime as the lookup table size, e.g. 37. More primes [here](https://www.bigprimes.net/archive/prime/).
