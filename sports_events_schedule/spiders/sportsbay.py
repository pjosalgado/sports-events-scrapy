# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime, timedelta
import pytz
from scrapy.exceptions import UsageError

class SportsBaySpider(scrapy.Spider):

    name = 'sportsbay'
    
    start_urls = [
        # Baseball
        'https://sportsbay.org/competition/mlb-baseball', 
        
        # Basketball
        'https://sportsbay.org/competition/euroleague-basketball', 
        'https://sportsbay.org/competition/nba-basketball', 
        
        # Football
        'https://sportsbay.org/competition/brazilian-serie-a', 
        'https://sportsbay.org/competition/concacaf-champions-league', 
        'https://sportsbay.org/competition/copa-libertadores', 
        'https://sportsbay.org/competition/english-league-cup', 
        'https://sportsbay.org/competition/english-premier-league', 
        'https://sportsbay.org/competition/french-ligue-1', 
        'https://sportsbay.org/competition/german-bundesliga', 
        'https://sportsbay.org/competition/italian-serie-a', 
        'https://sportsbay.org/competition/mls-soccer', 
        'https://sportsbay.org/competition/portuguese-primeira-liga', 
        'https://sportsbay.org/competition/spanish-la-liga', 
        'https://sportsbay.org/competition/uefa-champions-league', 
        'https://sportsbay.org/competition/uefa-champions-league-qualifying', 
        'https://sportsbay.org/competition/uefa-europa-league', 
        'https://sportsbay.org/competition/uefa-europa-league-qualifying', 
        'https://sportsbay.org/competition/uefa-nations-league', 
        
        # Hockey
        'https://sportsbay.org/competition/nhl-hockey', 
        
        # Motorsports
        'https://sportsbay.org/competition/formula-1', 
        
        # NFL
        'https://sportsbay.org/competition/nfl-football',
        
        # Tennis
        'https://sportsbay.org/competition/australian-open', 
        'https://sportsbay.org/competition/us-open', 
    ]
    
    TIMEZONE = pytz.timezone('America/Sao_Paulo')
    
    
    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs): 
        
        try: 
            start_in_days = int(kwargs['START_IN_DAYS'])
        except: 
            raise UsageError('START_IN_DAYS not found in args')
        
        print('START_IN_DAYS', start_in_days)
        date_start = datetime.now(cls.TIMEZONE).date() + timedelta(days=start_in_days)
        date_start = datetime.combine(date_start, datetime.min.time(), cls.TIMEZONE)
        print('date_start', date_start)
        
        try: 
            qty_plus_days = int(kwargs['QTY_PLUS_DAYS'])
        except: 
            raise UsageError('QTY_PLUS_DAYS not found in args')

        print('QTY_PLUS_DAYS', qty_plus_days)
        date_max = date_start + timedelta(days=qty_plus_days)
        date_max = datetime.combine(date_max, datetime.max.time(), cls.TIMEZONE)
        print('date_max', date_max)
        
        spider = cls(
            *args, 
            date_start=date_start, 
            date_max=date_max, 
            **kwargs
        )
        
        spider._set_crawler(crawler)
        
        return spider
    
    
    def parse(self, response): 
        
        url = response.url
        print('visited <{}>'.format(url))

        timestamp = datetime.now(self.TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')

        to_continue = True

        for event in response.css('tbody > .vevent'): 

            time = event.css('.time > .value-title::attr(title)').get().strip()
            time = datetime.strptime(time, '%Y-%m-%dT%H:%M%z')
            time = time.astimezone(self.TIMEZONE)
            
            competition = event.css('.competition > .description::text').get().strip()
            event_summary = event.css('.summary::text').get().strip()

            if time < self.date_start: 
                print('Skipping <{}> because is not yet on date_start (<{}> before <{}>)'.format(event_summary, time, self.date_start))
                continue
            elif time > self.date_max: 
                print('Reached date_max on event <{}> (<{}> after <{}>)'.format(event_summary, time, self.date_max))
                to_continue = False
                break

            url = event.css('.url::attr(href)').get().strip()
            url = response.urljoin(url)

            yield {
                'spider': self.name, 
                'spider_pretty_name': 'SportsBay', 
                'spider_url': url, 
                'timestamp': timestamp, 
                'time': time.strftime('%d/%m/%Y %H:%M'), 
                'competition': competition, 
                'event': event_summary, 
                'url': url
            }
        
        next_page = response.css('.next::attr(href)').get()
        
        if next_page and to_continue: 
            next_page = response.urljoin(next_page.strip())
            print('next page is <{}>'.format(next_page))
            yield scrapy.Request(next_page)
