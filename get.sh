#!/bin/sh

year=62

if [ ! -e cookies.txt ]; then
    echo 'Error: cookies.txt is not found.' >&2
    exit 1
fi

if [ -e tmp ]; then
    echo 'Error: directory tmp already exists.' >&2
    exit 1
fi

if [ -e kif ]; then
    echo 'Error: directory kif already exists.' >&2
    exit 1
fi

mkdir -p tmp
mkdir -p kif
touch tmp/tmp

while :
do
    for class in M7 A1 B1 B2 C1 C2;
    do
	wget -w 1 --random-wait --load-cookies cookies.txt http://member.meijinsen.jp/pay/game_list/meijinsen/${year}/${class}/calendar.html -O tmp/${year}_${class}.html
    done
    if [ ! "$?" -eq 0 ]; then
	break
    fi
    year=$(( $year + 1 ))
done

for class in M7 A1 B1 B2 C1 C2; do
    wget -w 1 --random-wait --load-cookies cookies.txt http://member.meijinsen.jp/pay/game_list/meijinsen/latest/${class}/calendar.html -O tmp/latest_${class}.html
done

for file in `ls tmp/*.html`;
do
    grep -o -E "'/pay/kif/meijinsen/[0-9]{4}/[0-9]{2}/[0-9]{2}/../[0-9]+.html'" ${file} >> tmp/tmp
done

sed "s/'//g" tmp/tmp | sort -u > tmp/kiflist
rm tmp/tmp

for file in `cat tmp/kiflist`;
do
    wget -w 1 --random-wait -q --load-cookies cookies.txt http://member.meijinsen.jp/${file} -O tmp/tmp;
    filehead=`echo ${file} | sed "s/[0-9]*\.html//g"`
    for idx in `grep -o -E "[0-9]+.(txt|html)" tmp/tmp | cut -d '.' -f 1,1 | sort -u`;
    do
	wget -w 1 --random-wait --load-cookies cookies.txt http://member.meijinsen.jp${filehead}${idx}.txt -P kif/
    done
done

rm -r tmp
