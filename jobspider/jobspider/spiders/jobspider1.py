# -*- coding: utf-8 -*-
import scrapy
from jobspider.items import JobspiderItem

class Jobspider1Spider(scrapy.Spider):
    name = 'jobspider1'
    #allowed_domains = ['http://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=']
    start_urls = ['http://search.51job.com/list/080200,000000,0000,00,9,99,Python,2,1.html?lang=c&stype=&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&providesalary=99&lonlat=0%2C0&radius=-1&ord_field=0&confirmdate=9&fromType=&dibiaoid=0&address=&line=&specialarea=00&from=&welfare=/']

    def parse(self, response):
        item = JobspiderItem()
        for each in response.css(" div.dw_table div.el")[1:]:
        	item["title"] = each.css("p.t1 a::attr(title)").extract_first()
        	item["companyname"] = each.css("span.t2 a::attr(title)").extract_first()
        	item["location"] = each.css("span.t3::text").extract_first()
        	item["salary"] = each.css("span.t4::text").extract_first()
        	item["date"] = each.css("span.t5::text").extract_first()

        	yield item

        next_page = response.css("div.dw_page li.bk a::attr(href)")[-1].extract()
        if next_page is not None:
        	yield response.follow(url=next_page,callback=self.parse)