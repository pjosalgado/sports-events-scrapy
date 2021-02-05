#!/bin/bash

args='-a START_IN_DAYS=0 -a QTY_PLUS_DAYS=0'
settings="-s TELEGRAM_TOKEN=$TELEGRAM_TOKEN -s TELEGRAM_CHAT_ID=$TELEGRAM_CHAT_ID"

rm -f outputs/sportsbay.csv
scrapy crawl sportsbay ${args} ${settings} -o outs/sportsbay-$(date +'%Y-%m-%d-%H-%M-%S').csv
