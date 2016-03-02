#!/bin/sh

TARGET=kif
CLEAN=kif_clean

if [ -e ${CLEAN} ]; then
    mkdir -p ${CLEAN}
fi

for file in `ls ${TARGET}`;
do
    python jisx/cleansing.py ${TARGET}/${file} > ${CLEAN}/${file}
done
