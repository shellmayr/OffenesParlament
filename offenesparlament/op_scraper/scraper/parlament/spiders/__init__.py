import scrapy

import feedparser
import roman
from urllib import urlencode
from ansicolor import red
from ansicolor import cyan
from ansicolor import green
from ansicolor import blue


class BaseSpider(scrapy.Spider):

    """
    Base class for scraping parliamentary sites
    """

    # Law Periods/Gesetzgebungsperioden to scrape
    LLP = [20, 21, 22, 23, 24, 25]

    # Basic URL after host to scrape (must be rss)
    BASE_URL = ""

    # Options dictionary for rss url
    URLOPTIONS = {}

    allowed_domains = ["parlament.gv.at"]

    def __init__(self, **kw):
        super(BaseSpider, self).__init__(**kw)

        # shut off annoying debug level core api messages
        import scrapy
        scrapy.core.engine.logger.setLevel('INFO')

    def print_debug(self):
        """
        Collects and prints a structured debug message
        """
        message = """
    {bar}

    {title}

      Scraping LLPs: {llps}
      Base URL:      {url}

    {bar}
        """.format(
            bar=cyan(
                '############################################################'),
            title=red(self.title),
            llps=self.LLP or "Not applicable",
            url=self.BASE_URL
        )
        print message

    def get_urls(self):
        """
        Returns a list of URLs to scrape
        """
        urls = []
        if self.LLP:
            for i in self.LLP:
                roman_numeral = roman.toRoman(i)
                options = self.URLOPTIONS.copy()
                options['GP'] = roman_numeral
                url_options = urlencode(options)
                url_llp = "{}?{}".format(self.BASE_URL, url_options)
                rss = feedparser.parse(url_llp)

                print "GP {}: {} laws".format(
                    roman_numeral, len(rss['entries']))
                urls = urls + [entry['link'] for entry in rss['entries']]

        return urls
