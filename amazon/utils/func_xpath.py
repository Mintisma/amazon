def get_price(response):
    try:
        price = float(response.xpath('//span[@id="priceblock_ourprice"]/text()').extract_first('').replace('$', ''))
        if price:
            return price
    except Exception as e:
        try:
            price = float(response.xpath('//span[@id="priceblock_saleprice"]/text()').extract_first('').replace('$', ''))
            if price:
                return price
        except Exception as e:
            print('review_star error')
    return 0


