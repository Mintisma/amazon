from urllib.parse import urljoin
from time import time

from amazon.settings import country_query_url_dict


def refresh_url_qid(url):
    if 'qid' in url:
        qid_start = url.index('qid') + 4
        qid_end = qid_start + 10
        url = url[:qid_start] + str(round(time())) + url[qid_end:]
    return url


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


def get_search_price(product, country):
    if country == 'us':
        price = get_us_price(product)
    elif country == 'de':
        price = get_de_price(product)
    elif country == 'fr':
        price = get_fr_price(product)
    elif country == 'uk':
        price = get_uk_price(product)
    else:
        raise KeyError('country should be one of us, de, fr, uk')

    return price


def get_detail_rating(response):
    try:
        rating = response.xpath('//span[@id="acrPopover"]/span/a/i/span/text()').extract_first(0)
        rating = float(rating.split()[0].replace(',', '.'))
    except:
        rating = 0
    return rating


def get_detail_reviews(response):
    try:
        reviews = response.xpath('//span[@id="acrCustomerReviewText"]/text()').extract_first('')
        reviews = int(reviews.split()[0].replace(',', ''))
    except:
        reviews = 0
    return reviews


def get_detail_url(product, country):

    base_url = country_query_url_dict[country]
    # base_url = 'https://www.amazon.com/s?k='

    url_extend = product.xpath('div/span/div/div/span/a[@class="a-link-normal"]/@href').extract_first('')
    if url_extend:
        url_extend = '/'.join(url_extend.split('/')[:-1])
    else:
        url_extend = product.xpath('div/span/div/div/div[2]/div/div/div/span/a/@href').extract_first('')

    url = urljoin(base_url, url_extend)
    url = refresh_url_qid(url)
    return url


def get_us_price(product):
    try:
        price = float(product.xpath('div/span/div/div/div[contains(@class, "a-spacing-top-mini")]/div/span[@dir="auto" and @class="a-color-base"]/text()').extract_first('').replace('$', '').replace(',', '').replace('€', ''))
    except:
        try:
            price_raw = product.xpath('div/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]')[-1]
            price = float(price_raw.xpath('div/div/a/span/span[@class="a-offscreen"]/text()').extract_first('').replace('$', '').replace(',', ''))
        except:
            try:
                price = float(product.xpath('.//span[@class="a-price-whole"]/text()').extract_first().replace(',', '') + '.' + product.xpath('.//span[@class="a-price-fraction"]/text()').extract_first())
            except:
                price = 0

    return price


def get_de_price(product):
    try:
        price = float(product.xpath('.//span[@class="a-price-whole"]/text()').extract_first().replace(',', '.').replace('.', ''))
    except:
        try:
            price = float(product.xpath('div/span/div/div/div[contains(@class, "a-spacing-top-mini")]/div/span[@dir="auto" and @class="a-color-base"]/text()').extract_first('').replace(',', '.').replace('.', '').replace('€', ''))
        except:
            try:
                price_raw = product.xpath('div/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]')[-1]
                price = float(price_raw.xpath('div/div/a/span/span[@class="a-offscreen"]/text()').extract_first('').replace('€', '').replace(',', '.').replace('.', ''))
            except:
                price = 0

    return price


def get_fr_price(product):
    try:
        price = float(product.xpath('.//span[@class="a-price-whole"]/text()').extract_first().replace(' ', '').replace(',', '.'))
    except:
        try:
            price = float(product.xpath('div/span/div/div/div[contains(@class, "a-spacing-top-mini")]/div/span[@dir="auto" and @class="a-color-base"]/text()').extract_first('').replace(' ', '').replace(',', '.').replace('€', ''))
        except:
            try:
                price_raw = product.xpath('div/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]')[-1]
                price = float(price_raw.xpath('div/div/a/span/span[@class="a-offscreen"]/text()').extract_first('').replace('€', '').replace(' ', '').replace(',', '.'))
            except:
                price = 0

    return price


def get_uk_price(product):
    try:
        price = float(product.xpath('.//span[@class="a-price-whole"]/text()').extract_first().replace(',', '') + '.' + product.xpath('.//span[@class="a-price-fraction"]/text()').extract_first())
    except:
        try:
            price = float(product.xpath('div/span/div/div/div[contains(@class, "a-spacing-top-mini")]/div/span[@dir="auto" and @class="a-color-base"]/text()').extract_first('').replace(',', '').replace('£', ''))
        except:
            try:
                price_raw = product.xpath('div/span/div/div/div[@class="a-section a-spacing-none a-spacing-top-small"]')[-1]
                price = float(price_raw.xpath('div/div/a/span/span[@class="a-offscreen"]/text()').extract_first('').replace('€', '').replace(',', '.'))
            except:
                price = 0

    return price

