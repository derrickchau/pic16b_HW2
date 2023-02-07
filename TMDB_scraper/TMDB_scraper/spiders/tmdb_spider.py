#!/usr/bin/env python
# coding: utf-8

# In[35]:


# to run 
# scrapy crawl tmdb_spider -o movies.csv

import scrapy

class TmdbSpider(scrapy.Spider):
    name = 'tmdb_spider'
    
    start_urls = ['https://www.themoviedb.org/movie/634649-spider-man-no-way-home']
    
    def parse(self, response):
        
        cast_url = response.request.url + "/cast"
        yield scrapy.Request(cast_url, callback = self.parse_full_credits)

        
    def parse_full_credits(self, response):
        cast = response.css('section.panel.pad')[0]
        actorList = [a.attrib['href'] for a in cast.css('ol.people.credits a')] # a
        
        for actor in actorList:
            actorPages = "https://www.themoviedb.org" + actor
            yield scrapy.Request(actorPages, callback = self.parse_actor_page)

        
    def parse_actor_page(self, response):
        actingHistory = response.css('table.card.credits')[0]
        actorName = response.css("h2.title a::text").get()

        for acts in actingHistory.css("td.role.false.account_adult_false.item_adult_false"):
                yield {"actor" : actorName,
                        "movie_or_TV_name" : acts.css("bdi::text").get()}


# In[ ]:




