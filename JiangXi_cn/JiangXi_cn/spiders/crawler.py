import json

import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CrawlerSpider(CrawlSpider):
    name = "crawler"
    allowed_domains = ["www.jxsggzy.cn"]

    start_urls = ["https://www.jxsggzy.cn/"]

    rules = (Rule(
        # 进入详情页
        LinkExtractor(restrict_xpaths=''), callback="parse_item", follow=True),

    )

    def parse_start_url(self, response):
        """处理初始请求（start_urls）的response"""
        # 今日公告信息
        today_trade = response.xpath('//a[@class="today-trade-card"]')
        for element in today_trade:

            name = element.xpath('p/text()').get() # 保存为集合
            bidding_announcement_equal =str(element.xpath('div/p[1]/@data-url').get().split('/')[3])
            win_bid_pub_equal = str(element.xpath('div/p[2]/@data-url').get().split('/')[3])
            print(type(bidding_announcement_equal))
            data_bidding = {
                        "token": "",
                        "pn": 0,
                        "rn": 10,
                        "sdt": "",
                        "edt": "",
                        "wd": "",
                        "inc_wd": "",
                        "exc_wd": "",
                        "fields": "",
                        "cnum": "",
                        "sort": "{\"webdate\":\"0\",\"id\":\"0\"}",
                        "ssort": "",
                        "cl": 500,
                        "terminal": "",
                        "condition": [
                            {
                                "fieldName": "categorynum",
                                "equal": bidding_announcement_equal,
                                "notEqual": None,
                                "equalList": None,
                                "notEqualList": None,
                                "isLike": True,
                                "likeType": 2
                            }
                        ],
                        "time": [
                            {
                                "fieldName": "webdate",
                                "startTime": "2025-06-11 00:00:00",
                                "endTime": "2025-06-11 23:59:59"
                            }
                        ],
                        "highlights": "",
                        "statistics": None,
                        "unionCondition": [],
                        "accuracy": "",
                        "noParticiple": "1",
                        "searchRange": None,
                        "noWd": True
                    }
            data_win = {
                "token": "",
                "pn": 0,
                "rn": 10,
                "sdt": "",
                "edt": "",
                "wd": "",
                "inc_wd": "",
                "exc_wd": "",
                "fields": "",
                "cnum": "",
                "sort": "{\"webdate\":\"0\",\"id\":\"0\"}",
                "ssort": "",
                "cl": 500,
                "terminal": "",
                "condition": [
                    {
                        "fieldName": "categorynum",
                        "equal": win_bid_pub_equal,
                        "notEqual": None,
                        "equalList": None,
                        "notEqualList": None,
                        "isLike": True,
                        "likeType": 2
                    }
                ],
                "time": [
                    {
                        "fieldName": "webdate",
                        "startTime": "2025-06-11 00:00:00",
                        "endTime": "2025-06-11 23:59:59"
                    }
                ],
                "highlights": "",
                "statistics": None,
                "unionCondition": [],
                "accuracy": "",
                "noParticiple": "1",
                "searchRange": None,
                "noWd": True
            }
            """
            配置1·招标和2·中标，不能同时运行！！！
            取消注释
            """
            #  1·进入招标公告详情页，指定回调函数（处理该链接的响应）
            # yield scrapy.Request(
            #     url='https://www.jxsggzy.cn/XZinterface/rest/esinteligentsearch/getFullTextDataNew',
            #     callback=self.parse_item,
            #     method='POST',
            #     body=json.dumps(data_bidding),
            #     meta={'from_page': response.url,'name':name}  # 可选：传递元数据（如来源页面）
            # )
            # 2·进入中标公示详情页，指定回调函数（处理该链接的响应）
            # yield scrapy.Request(
            #     url='https://www.jxsggzy.cn/XZinterface/rest/esinteligentsearch/getFullTextDataNew',
            #     callback=self.parse_win_item,
            #     method = 'POST',
            #     body=json.dumps(data_win),
            #     meta={'from_page': response.url, 'name': name} # 可选：传递元数据（如来源页面）
            # )








    def parse_item(self, response):
        item = {}
        name = response.meta.get('name')
        item['name'] = name

        data: dict = json.loads(response.text)['result']['records']
        for i in data:
            project = i['title']
            time = i['infodate']
            content = i['content']
            item['发布时间'] = time
            item['招标项目'] = project
            item['招标资质'] = content
            yield item

    def parse_win_item(self, response):
        item = {}
        name = response.meta.get('name')
        item['name'] = name

        data: dict = json.loads(response.text)['result']['records']
        for i in data:
            project = i['title']
            time = i['infodate']
            content = i['content']
            item['发布时间'] = time
            item['项目'] = project
            item['中标者'] = content
            yield item


