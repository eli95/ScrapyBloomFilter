import time
import logging

from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from . import defaults
from .connection import get_redis_from_settings
from .bloomfilter import BloomFilter


logger = logging.getLogger(__name__)


class RedisDupeFilter(BaseDupeFilter):
    logger = logger
    
    def __init__(self, server, key, debug, bit, hash_number):
        self.server = server
        self.key = key
        self.debug = debug
        self.bit = bit
        self.hash_number = hash_number
        self.logdupes = True
        self.bf = BloomFilter(server, self.key, bit, hash_number)
    
    @classmethod
    def from_settings(cls, settings):
        server = get_redis_from_settings(settings)
        key = defaults.DUPEFILTER_KEY % {'timestamp': int(time.time())}
        debug = settings.getbool('DUPEFILTER_DEBUG', defaults.DUPEFILTER_DEBUG)
        bit = settings.getint('BLOOMFILTER_BIT', defaults.BLOOMFILTER_BIT)
        hash_number = settings.getint('BLOOMFILTER_HASH_NUMBER', defaults.BLOOMFILTER_HASH_NUMBER)
        return cls(server, key=key, debug=debug, bit=bit, hash_number=hash_number)
    
    @classmethod
    def from_crawler(cls, crawler):
        """Returns instance from crawler.

        Parameters
        ----------
        crawler : scrapy.crawler.Crawler

        Returns
        -------
        RFPDupeFilter
            Instance of RFPDupeFilter.

        """
        instance = cls.from_settings(crawler.settings)
        return instance
    
    def request_seen(self, request):
        """Returns True if request was already seen.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        bool

        """
        fp = self.request_fingerprint(request)
        if self.bf.exists(fp):
            return True
        self.bf.insert(fp)
        return False
    
    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.

        Parameters
        ----------
        request : scrapy.http.Request

        Returns
        -------
        str

        """
        return request_fingerprint(request)
    
    def close(self, reason=''):
        """Delete data on close. Called by Scrapy's scheduler.

        Parameters
        ----------
        reason : str, optional

        """
        self.clear()
    
    def clear(self):
        """Clears fingerprints data."""
        self.server.delete(self.key)
    
    def log(self, request, spider):
        """Logs given request.

        Parameters
        ----------
        request : scrapy.http.Request
        spider : scrapy.spiders.Spider

        """
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False
        spider.crawler.stats.inc_value('bloomfilter/filtered', spider=spider)

