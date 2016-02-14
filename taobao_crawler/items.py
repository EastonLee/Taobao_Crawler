from scrapy.item import Item, Field
from scrapy.loader import XPathItemLoader
from scrapy.loader.processors import TakeFirst
import scrapy

class Website(Item):
    name = Field()
    description = Field()
    url = Field()

class WebsiteLoader(scrapy.loader.ItemLoader):
    default_item_class = Website
    default_output_processor = TakeFirst()

class Brand(Item):
    name = Field()
    url = Field()

class Model(Item):
    brand = Field()
    model = Field()
    no_of_seller = Field()
    price = Field()
    power = Field()

# TODO: below is todo
class Product(Item):
    product_id = Field()
    sales = Field()
    current_price = Field()

class Price(Item):
    current_time = Field()
    price = Field()

class Comment(Item):
    product_id = Field()
    comment = Field()