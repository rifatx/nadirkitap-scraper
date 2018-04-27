#!/bin/bash

rm -rf sahaflar.json
scrapy runspider BookshopListSpider.py -o sahaflar.json
jq -r ".[] | .url" sahaflar.json | xargs -L1 -i echo url={} | xargs -L1 -i scrapy runspider BookshopSpider.py -o kitaplar.json -a {}