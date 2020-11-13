import scrapy
from amazon_scraper.items import AmazonScraperItem


class ItemsSpiderSpider(scrapy.Spider):
    name = "items_spider"
    start_urls = [
        "https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250227011%2Cp_n_feature_browse-bin%3A2656020011&dc&fst=as%3Aoff&qid=1604604928&rnid=618072011&ref=sr_nr_p_n_feature_browse-bin_2"
    ]

    def parse(self, response, **kwargs):
        items = AmazonScraperItem()
        products = response.css("span div.s-latency-cf-section")
        for product in products:
            name = product.css(".a-color-base.a-text-normal::text").get()
            author = (
                product.css(".a-color-secondary .a-size-base.a-link-normal")
                .css("::text")
                .get()
            )
            price = (
                product.css(
                    ".a-spacing-top-small .a-price-fraction , .a-spacing-top-small .a-price-whole"
                )
                .css("::text")
                .extract()
            )
            image_link = product.css(".s-image::attr(src)").get()

            items["name"] = name
            items["author"] = author
            items["price"] = price
            items["image_link"] = image_link
            yield items

        next_href = response.css(".a-last a::attr(href)").get()
        if next_href is not None:
            yield response.follow(next_href, callback=self.parse)
