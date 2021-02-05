# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from pydispatch import dispatcher
from scrapy import signals
import requests
from urllib.parse import quote as parsequote
from itertools import groupby
from operator import itemgetter

class AggregateResultPipeline(object): 
    
    def __init__(self, telegram_token, telegram_chat_id): 
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        self.telegram_token = telegram_token
        self.telegram_chat_id = telegram_chat_id
        self.events = []
    
    @classmethod
    def from_crawler(cls, crawler): 
        return cls(
            telegram_token = crawler.settings.get('TELEGRAM_TOKEN'), 
            telegram_chat_id = crawler.settings.get('TELEGRAM_CHAT_ID')
        )
    
    def process_item(self, item, spider): 
        self.events.append(item)
        return item
    
    def send_telegram_message(self, message): 
        url = 'https://api.telegram.org/bot' + self.telegram_token + '/sendMessage?chat_id=' + self.telegram_chat_id + '&parse_mode=Markdown&text=' + message
        requests.get(url)
    
    def spider_closed(self, spider): 
        
        competition_fn = itemgetter('competition')
        events_sorted = sorted(self.events, key = competition_fn)
        result = {}
        
        for competition, events in groupby(events_sorted, key=competition_fn): 
            message = '*{}*\n'.format(competition)
            for event in events: 
                message += '- {}: [{}]({})\n'.format(event['time'], event['event'], event['url'])
            message = parsequote(message)
            self.send_telegram_message(message)
