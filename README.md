merging-triplets
================

A set of files for solving the problem listed here: http://stackoverflow.com/questions/22222994/optimal-merging-of-triplets

Usage
=====

### `merge_triplets.py`

 - `./merge_triplets.py < triplets` will merge triplets listed in the file `triplets`  with lookahead 3 and output the size of the resulting set.
 - `./merge_triplets.py -v < triplets` will output information on every step of the algorithm, visualizing recursion.
 - `./merge_triplets.py 0 < triplets` will use zero lookahead, a.k.a. the blind algorithm as discussed on StackOverflow.
 - `./merge_triplets.py 1 < triplets` will use the simple heuristic, a.k.a Level 1: Greedy.
 - `./merge_triplets.py 2 < triplets` also for any argument larger than 1, this will use the recursive lookahead algorithm a.k.a. Level 2: Very greedy

### `random_triplets.py`

 - `./random_triplets.py n` will generate `n` triplets on stdout, with maximum element value about base-3 logarithm of `n`
 - `./random_triplets.py | ./merge_triplets.py` is a convinient way of combining the two scripts

### `find_diff.sh`

 - `./find_diff.sh n l1 l2` will repeatedly generate sets of `n` triplets, and compare the results of merges with lookaheads `l1` and `l2` to find differences. When a difference is found, the script prints details of the event as well as the triplets that caused it and exits. Default values for `n`, `l1` and `l2` are `10`, `2` and `3` respectively.

### `stat_diff.sh`

 - `./stat_diff.sh n l1 l2` will do the same thing as `./find_diff.sh n l1 l2` except that instead of exiting, it will keep track of differences and continue running with new datasets. Sending an interrupt (Ctrl-C) will cause the script to print the statistics so far and exit. The script will leave behind `last_better[12]_triplets` files (so long the corresponding datasets have been found) so that they can be analyzed after the script has finished.

### `proof*` files

 - These files are examples of triplets which cause different results for different lookaheads, as found by the `find_diff.sh` script.
