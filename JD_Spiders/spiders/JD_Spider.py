import json
import random
import re

import requests
import scrapy
from scrapy import Request
from scrapy.linkextractors import LinkExtractor

from JD_Spiders.items import CategoryItem, ShopItem, ProductsItem
from JD_Spiders.share import html_from_uri


class JdSpiderSpider(scrapy.Spider):
    name = 'JD_Spider'
    allowed_domains = ['jd.com']
    start_urls = ['https://www.jd.com/allSort.aspx']

    key_word = ['book', 'e', 'channel', 'mvd', 'list']
    base_url = 'https://list.jd.com'
    price_url = 'https://p.3.cn/prices/mgets?skuIds=J_{product_id}'
    comment_url = 'https://club.jd.com/comment/productPageComments.action?productId={productId}&score=0&sortType=5&page={page}&pageSize=10'
    favourable_url = 'https://cd.jd.com/promotion/v2?skuId={skuId}&area=1_72_2799_0&shopId={shopId}&venderId={venderId}&cat={cat}'

    def parse(self, response):
        self.logger.debug('response.url: {}'.format(response.url))
        try:
            total = response.xpath('//div[@class="category-items clearfix"]//div[@class="category-item m"]')
            # le = LinkExtractor(
            #     restrict_xpaths='//div[@class="category-item m"]/div[@class="mc"]/div[@class="items"]/dl/dd/a')
            # links = le.extract_links(response)
            for t in total:
                first_category_name = t.xpath('./div[@class="mt"]/h2/span/text()').extract_first()
                second = t.xpath('./div[@class="mc"]/div[@class="items"]/dl')
                for s in second:
                    second_links = s.xpath('./dt/a').extract_first()
                    second_item = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a>', second_links)
                    self.logger.debug('second_item: {} '.format(second_item))
                    second_category_name = second_item[0][1]
                    second_category_url = 'https:' + second_item[0][0]
                    third_links = s.xpath('./dd/a').extract()
                    for third_link in third_links:
                        third_items = re.findall(r'<a href="(.*?)" target="_blank">(.*?)</a>', third_link)
                        self.logger.debug('third_items: {} '.format(third_items))
                        for item in third_items:
                            if item[0].startswith('https:'):
                                item[0] = item[0].lstrip('https:')
                            if item[0].split('.')[0].split('//')[1] != 'list':
                                self.logger.debug('not list url: {}'.format(item[0]))
                                yield Request('https:' + item[0], callback=self.parse_not_list)
                            else:
                                category_item = CategoryItem()
                                category_item['first_category_name'] = first_category_name
                                category_item['second_category_name'] = second_category_name
                                category_item['second_category_url'] = second_category_url
                                category_item['third_category_name'] = item[1]
                                category_item['third_category_url'] = 'https:' + item[0]
                                category_item['id'] = item[0].split('=')[1].split('&')[0]
                                yield category_item
                                category_info = {'first_category_name': first_category_name,
                                                 'second_category_name': second_category_name,
                                                 'third_category_name': item[1],
                                                 'third_category_id': item[0].split('=')[1].split('&')[0],
                                                 }
                                yield Request('https:' + item[0], callback=self.parse_list,
                                              meta={'category_info': category_info})
        except Exception as e:
            self.logger.debug('parse error:', e)

    def parse_not_list(self, response):
        pass

    def parse_list(self, response):
        category_info = response.meta.get('category_info')
        texts = response.xpath('//*[@id="plist"]/ul/li/div/div[@class="p-img"]/a').extract()
        for text in texts:
            items = re.findall(r'<a target="_blank" href="(.*?)">', text)
            yield Request(url='https:' + items[0], callback=self.parse_product, meta={'category_info': category_info})

        next_list = response.xpath('//a[@class="pn-next"]/@href').extract()
        if next_list:
            self.logger.debug('next page: {}'.format(self.base_url + next_list[0]))
            yield Request(url=self.base_url + next_list[0], callback=self.parse_list,
                          meta={'category_info': category_info})

    def parse_product(self, response):
        """商品页获取title,price,product_id"""
        category_info = response.meta.get('category_info')
        ids = re.findall(r"venderId:(.*?),\s.*?shopId:'(.*?)'", response.text)
        if not ids:
            ids = re.findall(r"venderId:(.*?),\s.*?shopId:(.*?),", response.text)
        vender_id = ids[0][0]
        shop_id = ids[0][1]

        # shop
        shopItem = ShopItem()
        shopItem['id'] = shop_id
        shopItem['venderId'] = vender_id
        shopItem['url1'] = 'http://mall.jd.com/index-%s.html' % (shop_id)
        try:
            shopItem['url2'] = 'https:' + \
                               response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/a/@href').extract_first()
        except:
            shopItem['url2'] = shopItem['url1']

        # name = ''
        if shop_id == '0':
            shopItem['name'] = '京东自营'
        else:
            if response.xpath('//ul[@class="parameter2 p-parameter-list"]/li/a//text()').extract_first():
                shopItem['name'] = response.xpath(
                    '//ul[@class="parameter2 p-parameter-list"]/li/a//text()').extract_first()
                self.logger.debug('name1: {}'.format(shopItem['name']))
            elif response.xpath('//span[@class="shop-name"]//text()').extract_first():
                shopItem['name'] = response.xpath('//span[@class="shop-name"]//text()').extract_first().strip()
                self.logger.debug('name2: {}'.format(shopItem['name']))
            elif response.xpath('//div[@class="name"]/a//text()').extract_first():
                self.logger.debug('name3 div[@class="name"]/a: {}'.format(response.xpath('//div[@class="name"]/a//text()').extract_first()))
                shopItem['name'] = response.xpath('//div[@class="name"]/a//text()').extract_first().strip()
                self.logger.debug('name3: {}'.format(shopItem['name']))
            elif response.xpath('//div[@class="shopName"]/strong/span/a//text()').extract_first():
                shopItem['name'] = response.xpath(
                    '//div[@class="shopName"]/strong/span/a//text()').extract_first().strip()
                self.logger.debug('name4: {}'.format(shopItem['name']))
            elif response.xpath('//div[@class="shopName"]/strong/span/a//text()').extract_first():
                shopItem['name'] = response.xpath(
                    '//div[@class="shopName"]/strong/span/a//text()').extract_first().strip()
                self.logger.debug('name5: {}'.format(shopItem['name']))
            elif response.xpath('//div[@class="seller-infor"]/a//text()').extract_first():
                shopItem['name'] = response.xpath('//div[@class="seller-infor"]/a//text()').extract_first().strip()
                self.logger.debug('name6: {}'.format(shopItem['name']))
            else:
                shopItem['name'] = '京东自营'
                self.logger.debug('name7: {}'.format(shopItem['name']))

        yield shopItem

        productsItem = ProductsItem()
        productsItem['shopId'] = shop_id
        productsItem['first_category_name'] = category_info.get('first_category_name')
        productsItem['second_category_name'] = category_info.get('second_category_name')
        productsItem['third_category_name'] = category_info.get('third_category_name')
        productsItem['third_category_id'] = category_info.get('third_category_id')
        # try:
        #     # title = response.xpath('//div[@class="sku-name"]/text()').extract()[0].replace(u"\xa0", "").strip()
        #     title = ''.join(response.xpath('//div[@class="sku-name"]//text()').extract())
        #     self.logger.debug('title1: {}'.format(title))
        # except Exception as e:
        #     title = response.xpath('//div[@id="name"]/h1/text()').extract_first()
        if response.xpath('//div[@class="sku-name"]/text()').extract():
            # title = ''.join(i.split() for i in response.xpath('//div[@class="sku-name"]//text()').extract())
            # title = ''.join(response.xpath('//div[@class="sku-name"]/text()').extract_first().split())
            title = ''.join(i.strip() for i in response.xpath('//div[@class="sku-name"]/text()').extract())
            self.logger.debug('title1: {}'.format(title))
        elif response.xpath('//div[@id="name"]/h1/text()').extract_first():
            title = response.xpath('//div[@id="name"]/h1/text()').extract_first()
            self.logger.debug('title2: {}'.format(title))
        else:
            title = response.xpath('//ul[@class="parameter2 p-parameter-list"]/li[1]/@title').extract_first()
            self.logger.debug('title3: {}'.format(title))
        productsItem['name'] = title.strip()
        product_id = response.url.split('/')[-1][:-5]
        productsItem['id'] = product_id
        productsItem['url'] = response.url

        # description
        desc = response.xpath('//ul[@class="parameter2 p-parameter-list"]//text()').extract()
        productsItem['description'] = '/'.join(i.strip() for i in desc)
        # productsItem['description'] = '/'.join(desc)

        # price
        # response = requests.get(url=price_url + product_id)
        # price_response = html_from_uri(self.price_url.format(product_id=product_id))
        total_price_url = self.price_url.format(product_id=product_id) + '&pduid=' + str(random.randint(100000, 999999))
        self.logger.debug('total_price_url: {}'.format(total_price_url))
        price_response = requests.get(total_price_url)
        price_json = price_response.json()
        self.logger.debug('price_json:{}'.format(price_json))
        productsItem['reallyPrice'] = price_json[0]['p']
        productsItem['originalPrice'] = price_json[0]['m']

        # 优惠
        # res_url = self.favourable_url % (product_id, shop_id, vender_id, category.replace(',', '%2c'))
        res_url = self.favourable_url.format(skuId=product_id, shopId=shop_id, venderId=vender_id,
                                             cat=category_info.get('third_category_id').replace(',', '%2c'))
        # print(res_url)
        # response = requests.get(res_url)
        # fav_response = html_from_uri(res_url)
        fav_response = requests.get(res_url)
        fav_data = fav_response.json()
        self.logger.debug('fav_data:{}'.format(fav_data))
        if fav_data['skuCoupon']:
            desc1 = []
            for item in fav_data['skuCoupon']:
                start_time = item['beginTime']
                end_time = item['endTime']
                time_dec = item['timeDesc']
                fav_price = item['quota']
                fav_count = item['discount']
                fav_time = item['addDays']
                desc1.append(u'有效期%s至%s,满%s减%s' % (start_time, end_time, fav_price, fav_count))
            productsItem['favourableDesc1'] = ';'.join(desc1)

        if fav_data['prom'] and fav_data['prom']['pickOneTag']:
            desc2 = []
            for item in fav_data['prom']['pickOneTag']:
                desc2.append(item['content'])
            productsItem['favourableDesc2'] = ';'.join(desc2)

        data = dict()
        data['product_id'] = product_id
        yield productsItem
        # yield Request(url=comment_url % (product_id, '0'), callback=self.parse_comments, meta=data)
