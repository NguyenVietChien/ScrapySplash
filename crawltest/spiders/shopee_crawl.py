from urllib.parse import urljoin
import scrapy
from scrapy_splash import SplashRequest
from ..items import ProductItem

# scrapy crawl shopee_crawl2
render_script2 = """
        function main(splash)
            splash.private_mode_enabled = false
            local url = splash.args.url
            splash:go(url)
            splash:wait(5)
            splash.indexeddb_enabled = true
            splash.html5_media_enabled = true
            splash:set_viewport_full()
            
            splash:wait(5)

            return {
                html = splash:html(),
                url = splash:url()
            }
        end
"""


class ShopeeCrawlSpider(scrapy.Spider):
    name = 'shopeecrawl'

    def __init__(self, *args, **kwargs):

        super(ShopeeCrawlSpider, self).__init__(*args, **kwargs)

        # self.url = kwargs.get('url')
        self.url = 'https://shopee.vn/search?keyword=%C4%91%E1%BB%93%20%C4%83n'
        print(self.url)
        # self.domain = kwargs.get('domain')
        # self.allowed_domains = [self.domain]
        self.start_urls = [self.url]

    page_number = 1

    item = ProductItem()

    render_script = '''
    function main(splash)
        splash:go(splash.args.url)
        assert(splash:wait(2))

        local num_scrolls = 10
        local scroll_delay = 1

        local scroll_to = splash:jsfunc("window.scrollTo")
        local get_body_height = splash:jsfunc(
            "function() {return document.body.scrollHeight;}"
        )

        for _ = 1, num_scrolls do
            local height = get_body_height()
            for i = 1, 10 do
                scroll_to(0, height * i/2)
                splash:wait(scroll_delay/10)
            end
        end

        assert(splash:wait(2))
        
        return {
            html = splash:html(),
            url = splash:url(),
        }
    end
    '''

    def start_requests(self):
        for url in self.start_urls:
            print(url)

            yield SplashRequest(
                url,
                endpoint="execute",
                args={
                    'wait': 0.5,
                    'url': url,
                    'lua_source': render_script2,
                    'viewport': '1024x2480',
                    'timeout': 90,
                    'images': 0,
                },
                callback=self.parse,
                dont_filter=True
            )

    def parse(self, response):
        # item = ProductItem()
        for data in response.css(".shopee-search-item-result__item"):
            # item["location"] = data.css("div.zGGwiV").extract_first()
            # item["name"] = data.css(".Cve6sh::text").extract_first()

            link = data.css('a::attr(href)').get()

            if link is not None:
                link = response.urljoin(link)
                # item["link"] = link

            request = SplashRequest(
                url=link,
                callback=self.parse_detail,
                # cb_kwargs=dict(item=item),
                meta={
                    "splash": {
                        "endpoint": "execute",
                        "args": {
                            'wait': 5,
                            'url': link,
                            'lua_source': render_script2,
                            'viewport': '1024x8480',
                            'timeout': 90,
                            'images': 0,
                        },
                    }
                },
                dont_filter=True
            )
            yield request

        total_page = response.css(
            '.shopee-mini-page-controller__total::text').extract_first()

        numpage = str(ShopeeCrawlSpider.page_number)
        next_page = self.url + "&page=" + numpage

        print(numpage + "-------" + str(total_page) + "-------" + next_page)

        if ShopeeCrawlSpider.page_number < 3:
            ShopeeCrawlSpider.page_number += 1
            yield SplashRequest(
                url=next_page,
                callback=self.parse,
                meta={
                    "splash": {
                        "endpoint": "execute",
                        "args": {
                            'wait': 5,
                            'url': response.url,
                            "lua_source": render_script2,
                        },
                    }
                },
                dont_filter=True
            )

    def parse_detail(self, response):

        # print(response.body.decode('utf8'))
        print("_______________________________________________________________________________________________")

        xpath_rating = '//*[@id="main"]/div/div[2]/div[1]/div/div/div[2]/div[3]/div[3]/div[1]/div[2]/div'
        rating = response.xpath(xpath_rating).getall()
        print(rating)

        yield {
            'result 1': rating,
        }
