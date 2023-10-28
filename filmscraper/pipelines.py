# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import certifi
ca = certifi.where()

class FilmscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        #
        # Photos
        for i in range(len(adapter['photos_url'])):
            curr = adapter['photos_url'][i]
            adapter['photos_url'][i] = ".".join(curr.split('.')[:-2]) + '.1.' + curr.split('.')[-1]

        # World & PL Premiere
        if adapter.get('world_premiere'):
            adapter['world_premiere'] = " ".join(adapter.get('world_premiere').split(' ')[1:-1]).replace("(Światowa i polska premiera kinowa)", "")
        if adapter.get('pl_premiere'):
            adapter['pl_premiere'] = " ".join(adapter.get('pl_premiere').split(' ')[1:-1]).replace("(Światowa i polska premiera kinowa)", "")

        return item

import pymongo
# from scrapy.conf import settings
from scrapy.exceptions import DropItem
# from scrapy import log

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, mongo_db_collection_name, mongo_username, mongo_user_password):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.mongo_db_collection_name = mongo_db_collection_name
        self.mongo_username = mongo_username
        self.mongo_user_password = mongo_user_password

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_db_collection_name=crawler.settings.get('MONGO_DATABASE_COLLECTION_NAME'),
            mongo_username=crawler.settings.get('MONGO_USERNAME'),
            mongo_user_password=crawler.settings.get('MONGO_USER_PASSWORD')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(
            self.mongo_uri, username=self.mongo_username, password=self.mongo_user_password,
            tlsCAFile=ca
        )
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.mongo_db_collection_name].insert_one(dict(item))
        return item