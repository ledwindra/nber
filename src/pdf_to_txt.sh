#!/bin/bash

export START=$1
export END=$2
export DIRECTORY="paper"

# create directory if does not exist
if [ ! -d $DIRECTORY ]; then
    mkdir $DIRECTORY
fi

# create a function to make an NBER ID
get_nber_id () {
    if (( $START < 10 )); then
        export NBER_ID="000${START}"
    elif (( $START >= 10 && $START < 100 )); then
        export NBER_ID="00${START}"
    elif (( $START >= 100 && $START < 1000 )); then
        export NBER_ID="0${START}"
    else
        export NBER_ID=${START}
    fi
}

# download paper -> .pdf
# parse .pdf to .txt
# remove .pdf
# iterate
while (( $START < $END ))
do
    get_nber_id
    if [ -e "${DIRECTORY}/${NBER_ID}.txt" ]
    then
        printf "[IGNORE 📁]: ${DIRECTORY}/${NBER_ID}.txt exists\n"
    else
        printf "[DOWNLOAD 💾]: ${DIRECTORY}/${NBER_ID}.pdf\n"
        python3 src/download_paper.py
        if [ -e "${DIRECTORY}/${NBER_ID}.pdf" ]
        then
            pdftotext -layout "${DIRECTORY}/${NBER_ID}.pdf" "${DIRECTORY}/${NBER_ID}.txt"
            rm -rf "${DIRECTORY}/${NBER_ID}.pdf"
            printf "[SUCCEED ✅]: ${DIRECTORY}/${NBER_ID}.txt\n"
        else
            printf "[FAIL 📭]: ${DIRECTORY}/${NBER_ID}.pdf is not found or access is denied\n"
        fi
    fi
    START=$(($START + 1))
done
