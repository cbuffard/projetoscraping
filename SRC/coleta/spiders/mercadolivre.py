import scrapy


class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-masculino"]   # request in the site 
    page_count = 1
    max_pages = 10

    def parse(self, response):
        products = response.css('div.ui-search-result__content')  # extract the block of each shoes/image from the site, 54 items 

        for product in products:      # extracting brand from each block
           
           prices = product.css('span.andes-money-amount__fraction::text').getall()   # full price
           cents = product.css('span.andes-money-amount__cents::text').getall()        # cents part price

           yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(),
                'name': product.css('h2 > a::text').get(),
                'old_price_reais': prices[0] if len(prices) > 0 else None,  # 'else' just in case there are no values avoiding the code to break
                'old_price_centavos': cents[0] if len(cents) > 0 else None,
                'new_price_reais': prices[1] if len(prices) > 1 else None,
                'new_price_centavos': cents[1] if len(cents) > 1 else None,
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(),
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get()

           }

        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)
