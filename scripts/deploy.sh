#!/bin/bash

cp scrapinghub.yml scrapinghub.temp.yml
rpl '$SHUB_API_KEY' $SHUB_API_KEY scrapinghub.yml

shub deploy

mv scrapinghub.temp.yml scrapinghub.yml
