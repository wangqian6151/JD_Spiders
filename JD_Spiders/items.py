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
    crawl_time = Field()


class ShopItem(Item):
    collection = table = 'Shop'

    id = Field()  #shop id
    name = Field()  #店铺名称
    url1 = Field()  #店铺url1
    url2 = Field()  #店铺url2
    venderId = Field()  #vender id
    crawl_time = Field()


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
    crawl_time = Field()


class CommentItem(Item):
    collection = table = 'Comment'

    id = Field()
    productId = Field()  #同ProductsItem的id相同
    guid = Field()
    content = Field()
    creationTime = Field()
    isTop = Field()
    referenceId = Field()
    referenceName = Field()
    referenceTime = Field()
    referenceType = Field()
    referenceTypeId = Field()
    firstCategory = Field()
    secondCategory = Field()
    thirdCategory = Field()
    replyCount = Field()
    score = Field()
    status = Field()
    title = Field()
    usefulVoteCount = Field()
    uselessVoteCount = Field()
    userImage = Field()
    userImageUrl = Field()
    userLevelId = Field()
    userProvince = Field()
    viewCount = Field()
    orderId = Field()
    isReplyGrade = Field()
    nickname = Field()
    userClient = Field()
    mergeOrderStatus = Field()
    discussionId = Field()
    productColor = Field()
    productSize = Field()
    imageCount = Field()
    integral = Field()
    userImgFlag = Field()
    anonymousFlag = Field()
    userLevelName = Field()
    plusAvailable = Field()
    mobileVersion = Field()
    recommend = Field()
    userLevelColor = Field()
    userClientShow = Field()
    isMobile = Field()
    days = Field()
    afterDays = Field()
    crawl_time = Field()


class CommentImageItem(Item):
    collection = table = 'CommentImage'

    id = Field()
    associateId = Field()  #和CommentItem的discussionId相同
    productId = Field()   #不是ProductsItem的id，这个值为0
    imgUrl = Field()
    available = Field()
    pin = Field()
    dealt = Field()
    imgTitle = Field()
    isMain = Field()
    jShow = Field()
    crawl_time = Field()


class CommentSummaryItem(Item):
    collection = table = 'CommentSummary'

    id = Field()
    goodRateShow = Field()
    poorRateShow = Field()
    poorCountStr = Field()
    averageScore = Field()
    generalCountStr = Field()
    showCount = Field()
    showCountStr = Field()
    goodCount = Field()
    generalRate = Field()
    generalCount = Field()
    skuId = Field()
    goodCountStr = Field()
    poorRate = Field()
    afterCount = Field()
    goodRateStyle = Field()
    poorCount = Field()
    skuIds = Field()
    videoCount = Field()
    poorRateStyle = Field()
    generalRateStyle = Field()
    commentCountStr = Field()
    commentCount = Field()
    productId = Field()  #同ProductsItem的id相同
    videoCountStr = Field()
    afterCountStr = Field()
    defaultGoodCount = Field()
    goodRate = Field()
    generalRateShow = Field()
    defaultGoodCountStr = Field()
    jwotestProduct = Field()
    maxPage = Field()
    testId = Field()
    score = Field()
    soType = Field()
    imageListCount = Field()
    crawl_time = Field()


class HotCommentTagItem(Item):
    collection = table = 'HotCommentTag'

    id = Field()
    name = Field()
    status = Field()
    rid = Field()
    productId = Field()
    count = Field()
    created = Field()
    modified = Field()
    type = Field()
    canBeFiltered = Field()
    stand = Field()
    crawl_time = Field()

