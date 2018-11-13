# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class CategoryItem(Item):
    collection = table = 'Category'

    first_category_name = Field()
    second_category_name = Field()
    second_category_url = Field()
    third_category_name = Field()
    third_category_url = Field()
    id = Field()


class ShopItem(Item):
    collection = table = 'Shop'

    id = Field()  #shop id
    name = Field()  #店铺名称
    url1 = Field()  #店铺url1
    url2 = Field()  #店铺url2
    venderId = Field()  #vender id


class ProductsItem(Item):
    collection = table = 'Products'

    first_category_name = Field()
    second_category_name = Field()
    third_category_name = Field()
    third_category_id = Field()
    name = Field()  #产品名称
    url = Field()  #产品url
    id = Field()  #产品id
    reallyPrice = Field()  #产品价格
    originalPrice = Field()  #原价
    description = Field()  #产品描述
    shopId = Field()  #shop id
    # venderId = Field()  #vender id
    # commentCount = Field()  #评价总数
    # goodComment = Field()  #好评数
    # generalComment = Field()  #中评数
    # poolComment = Field()  #差评数
    favourableDesc1 = Field()  #优惠描述1
    favourableDesc2 = Field()  #优惠描述2

