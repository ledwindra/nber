#!/bin/bash

# parameters
START=$1
END=$2
SLEEP=$3
USER_AGENT=$4
TIMEOUT=$5
WAIT=$6

# constant
DIRECTORY="paper"

# create directory if does not exist
if [ ! -d $DIRECTORY ]; then
    mkdir $DIRECTORY
fi

# create a function to make an NBER ID
get_nber_id () {
    if (( $START < 10 )); then
        NBER_ID="000${START}"
    elif (( $START >= 10 && $START < 100 )); then
        NBER_ID="00${START}"
    elif (( $START >= 100 && $START < 1000 )); then
        NBER_ID="0${START}"
    else
        NBER_ID=${START}
    fi
}

# download paper -> .pdf
# parse .pdf to .txt
# remove .pdf
# iterate
while (( $START < $END ))
do
    get_nber_id
    URL="https://www.nber.org/system/files/working_papers/w${NBER_ID}/w${NBER_ID}.pdf"
    if [ -e "${DIRECTORY}/${NBER_ID}.txt" ]
    then
        echo "${DIRECTORY}/${NBER_ID}.pdf already exists."
    else
        wget \
            --timeout=$TIMEOUT \
            --waitretry=$WAIT \
            --user-agent=$USER_AGENT \
            $URL -O "${DIRECTORY}/${NBER_ID}.pdf"
        STATUS=$?
        if (( $STATUS == 0 ))
        then
            printf "Done downloading, now let me sleep for ${SLEEP} seconds... \xF0\x9F\x98\xB4 \n"
        else
            printf "Failed downloading, now let me sleep for ${SLEEP} seconds... \xF0\x9F\x98\xB4 \n"
        fi
        sleep $SLEEP
        pdftotext -layout "${DIRECTORY}/${NBER_ID}.pdf" "${DIRECTORY}/${NBER_ID}.txt"
        rm -rf "${DIRECTORY}/${NBER_ID}.pdf"
    fi
    START=$(($START + 1))
done

# remove unwanted file
rm -rf =
