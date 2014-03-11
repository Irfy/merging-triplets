#!/bin/bash

t_no=${1:-10}
l1=${2:-2}
l2=${3:-3}
echo "Computing result statistics for lookaheads $l1 and $l2 with input size $t_no. Press Ctrl-C to stop and print statistics."

handler() {
    exit_requested=1
}

trap handler INT

better1=0
better2=0
equal=0

while [[ -z $exit_requested ]] ; do
    ./random_triplets.py $t_no > triplets 2>/dev/null
    r1=$(./merge_triplets.py $l1 < triplets 2>/dev/null)
    r2=$(./merge_triplets.py $l2 < triplets 2>/dev/null)
    if [[ $r1 < $r2 ]] ; then
        (( better1 += 1 ))
        cp triplets last_better1_triplets
    elif [[ $r1 > $r2 ]] ; then
        (( better2 += 1 ))
        cp triplets last_better2_triplets
    elif [[ $r1 == $r2 ]] ; then
        (( equal += 1 ))
    fi 
    echo -n .
done

echo
echo "Lookahead $l1 was better $better1 times"
echo "Lookahead $l2 was better $better2 times"
echo "They were equally good $equal times"
