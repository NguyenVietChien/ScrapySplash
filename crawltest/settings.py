
# import django
from shutil import which

import os
import sys

# DJANGO INTEGRATION

sys.path.append(os.path.dirname(os.path.abspath('.')))
# Do not forget the change iCrawler part based on your project name
# os.environ['DJANGO_SETTINGS_MODULE'] = 'myEcommerce.settings'

# This is required only if Django Version > 1.8
# django.setup()

BOT_NAME = 'crawltest'

SPIDER_MODULES = ['crawltest.spiders']
NEWSPIDER_MODULE = 'crawltest.spiders'


# Obey robots.txt rules
# ROBOTSTXT_OBEY = True
# PROXY_POOL_ENABLED = True
USER_AGENT = 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
ROBOTSTXT_OBEY = False


SPLASH_URL = 'http://localhost:8050'
# SPLASH_URL = 'http://192.168.99.100:8050'
DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'
HTTPCACHE_STORAGE = 'scrapy_splash.SplashAwareFSCacheStorage'
COOKIES_ENABLED = True
SPLASH_COOKIES_DEBUG = False
SPIDER_MIDDLEWARES = {
    'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
}

DOWNLOADER_MIDDLEWARES = {

    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,

    'scrapy_splash.SplashCookiesMiddleware': 723,
    'scrapy_splash.SplashMiddleware': 725,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 400,


    # 'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
    # 'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
    # 'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    # 'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

DOWNLOAD_DELAY = 4
