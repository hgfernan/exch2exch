#! /bin/sh 

# set -x

DATE=`date +"%Y/%m/%d, %H:%M:%S"`

URL='https://www.google.com/finance/converter?a=1&from=USD&to=BRL'

LINE=`curl $URL | grep currency_converter` 

USD2BRL=`echo $LINE | awk 'BEGIN{FS=">"}{print $3}' | awk '{print $1}'`

URL='https://www.google.com/finance/converter?a=1&from=BRL&to=USD'

LINE=`curl $URL | grep currency_converter` 

BRL2USD=`echo $LINE | awk 'BEGIN{FS=">"}{print $3}' | awk '{print $1}'`

echo $DATE", "$USD2BRL", "$BRL2USD