#! /bin/sh 


# set -x

DATE=`date +"%Y/%m/%d, %H:%M:%S"`

URL='http://www.x-rates.com/table/?from=USD&amount=1'
LINES=`curl $URL | grep BRL | grep rtRates`
echo $LINES

ULINE=`echo $LINES | awk '{print $3}'`
echo $ULINE

ULINE=`echo $ULINE | awk 'BEGIN{ FS=">"}{print $2}'`
echo $ULINE

USD=`echo $ULINE | awk 'BEGIN{FS="<"}{print $1}'`

echo $USD

BLINE=`echo $LINES | awk '{print $6}'`
echo $BLINE

BLINE=`echo $BLINE | awk 'BEGIN{ FS=">"}{print $2}'`
echo $BLINE

BRL=`echo $BLINE | awk 'BEGIN{FS="<"}{print $1}'`

echo $BRL

echo $DATE", "$USD", "$BRL

