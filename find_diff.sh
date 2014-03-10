#!/bin/bash -e

t_no=${1:-10}
l1=${2:-2}
l2=${3:-3}
echo "Lookahead $l1 and lookahead $l2 competing with input size $t_no"

while :; do
    ./random_triplets.py $t_no > triplets
    r1=$(./merge_triplets.py $l1 < triplets)
    r2=$(./merge_triplets.py $l2 < triplets)
    if [[ $r1 != $r2 ]] ; then
        echo
        echo "Difference found! Lookahead $l1 had a result of $r1, whilst lookahead $l2 had a result of $r2 for these triplets:"
        cat triplets
        break
    fi
    echo -n .
done
