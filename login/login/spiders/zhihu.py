# -*- coding: utf-8 -*-
import scrapy,json
from login.items import LoginItem


class ZhihuSpider(scrapy.Spider):
    name = "zhihu"
    allowed_domains = ["zhihu.com"]
    start_urls = ['https://www.zhihu.com/']

    def parse(self, response):
        _xsrf=""
        for e in response.css("input[name=_xsrf]"):
            _xsrf=e.css("::attr(value)").extract()[0]
            print "###########################\n%s" % _xsrf
            break
        return [scrapy.FormRequest(
                url="https://www.zhihu.com/login/email",
                formdata={
                "_xsrf":_xsrf,
                "email":"445083931@qq.com",
                "password":"xyd@1989",
                "remenber_me":"true"
                },
                callback=self.check_login
                )]
    def check_login(self,response):
        if json.loads(response.body)['r'] == 0:
            yield scrapy.Request("https://www.zhihu.com/",
                callback=self.page_content,
                dont_filter=True)
    def page_content(self,response):
        with open('first_page.html', 'wb') as f:
            f.write(response.body)
        print '######################[[[done]]]'
