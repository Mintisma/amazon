def get_price(response):
    try:
        price = float(response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first('').replace('$', ''))
        if price:
            return price
    except:
        try:
            price = float(response.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first('').replace('$', ''))
            if price:
                return price
        except Exception as e:
            print('review_star error')
    return 0


def get_search_price(product):
    try:
        price = float(product.xpath('div/span/div/div/div[contains(@class, "a-spacing-top-mini")]/div/span[@dir="auto" and @class="a-color-base"]/text()').extract_first('').replace('$', '').replace(',', ''))
    except:
        try:
            price_raw = product.xpath('div/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]')[-1]
            price = float(price_raw.xpath('div/div/a/span/span[@class="a-offscreen"]/text()').extract_first('').replace('$', '').replace(',', ''))
        except:
            try:
                price = float(product.xpath('.//span[@class="a-price-whole"]/text()').extract_first().replace(',','') + '.' + product.xpath('.//span[@class="a-price-fraction"]/text()').extract_first())
            except:
                price = 0
    return price
