

declare -a metrics=("KD_woR" "KD_wR" "SB_bpe1000" "SB_bpe750" "SB_w2v_1k" "SB_w2v_3k" "SB_w2v_7k" "SB_w2v" "SB_xlsr_fr" "SB_xlsr")

arraylength=${#metrics[@]}

for (( i=0; i<${arraylength}; i++ ));
do
    for (( j=$i+1; j<${arraylength}; j++ ));
    do
        echo "${metrics[$i]} ${metrics[$j]}"
        # if [ ! -d transcriptions/mess/${metrics[$i]}-${metrics[$j]} ] ; then
        #     mkdir transcriptions/mess/${metrics[$i]}-${metrics[$j]}
        # fi
        python harvester.py ${metrics[$i]} ${metrics[$j]}
    done
done

# You can access them using echo "${metrics[0]}", "${metrics[1]}" also
