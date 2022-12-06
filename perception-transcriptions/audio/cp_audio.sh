


while IFS= read -r line; do
    cp /users/troux/corpus/REPERE/clips/$line.wav .
done < datasets/audios.txt
