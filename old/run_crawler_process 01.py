import scrapy
from scrapy.crawler import CrawlerProcess
from pricebot.spiders.elgiganten_prices import ElgigantenSpider
from pricebot.spiders.power_links import PowerLinksSpider
from pricebot.spiders.power_prices import PowerPricesSpider
from pricebot.spiders.skousen_prices import SkousenSpider

process = CrawlerProcess()
process.crawl(ElgigantenSpider)
process.crawl(PowerPricesSpider)
process.crawl(SkousenSpider)
process.start()

# process.stop()

# process = CrawlerProcess()
# process.crawl(PowerLinksSpider)
# process.start()
# process.stop()

# process = CrawlerProcess()
# process.crawl(PowerPricesSpider)
# process.start()
# process.stop()
#
# process = CrawlerProcess()
# process.crawl(SkousenSpider)
# process.start()
# process.stop()
