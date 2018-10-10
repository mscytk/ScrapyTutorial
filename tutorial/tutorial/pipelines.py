# -*- coding: utf-8 -*-
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


# class TutorialPipeline(object):
#     def process_item(self, item, spider):
#         return item

# refer: https://stackoverflow.com/questions/31779995/how-to-give-custom-name-to-images-when-downloading-through-scrapy
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        #for image_url in item:
#        print(item['jpgurl'])
        yield scrapy.Request(item['jpgurl'], meta={'birdname': item["birdname"]})

    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            filename = request._url.rsplit("/", 1)[1]
            path = 'full/%s/%s' % (response.meta['birdname'], filename)
            self.store.persist_file(
                path, buf, info,
                meta={'width': width, 'height': height})
        return checksum