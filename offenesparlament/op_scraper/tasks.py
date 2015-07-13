from __future__ import absolute_import

import scrapy
from scrapy.crawler import CrawlerProcess

from celery import shared_task

import reversion
from django.db import transaction

DEFAULT_CRAWLER_OPTIONS = {
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
}


@shared_task
def scrape(spider):
    with transaction.atomic(), reversion.create_revision():
        process = CrawlerProcess(DEFAULT_CRAWLER_OPTIONS)
        process.crawl(spider)
        # the script will block here until the crawling is finished
        process.start()
    return