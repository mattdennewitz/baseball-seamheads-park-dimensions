# -*- coding: utf-8 -*-
import copy
from urllib.parse import urljoin

import scrapy

from ..items import Ballpark


class BallparksSpider(scrapy.Spider):
    name = 'ballparks'
    allowed_domains = ['seamheads.com']
    start_urls = (
        'http://www.seamheads.com/ballparks/index.php?sort=games1&active=Y&era=&state=',
    )

    def parse(self, response):
        table = response.css('div#content table.itable tr:not(:first-child)')

        for tr in table:
            ballpark = Ballpark()

            # extract name and detail url
            name_and_url = tr.xpath('./td[1]/a')
            href = name_and_url.xpath('@href').extract_first()
            ballpark['name'] = name_and_url.xpath('text()').extract_first()
            ballpark['location'] = tr.xpath('./td[2]/a/text()').extract_first()
            ballpark['lat'] = tr.xpath('./td[9]//text()').extract_first().strip()
            ballpark['lng'] = tr.xpath('./td[10]//text()').extract_first().strip()
            ballpark['altitude'] = tr.xpath('./td[11]//text()').extract_first().strip()

            detail_url = urljoin('http://www.seamheads.com/ballparks/', href)
            detail_req = scrapy.Request(detail_url,
                                        callback=self.parse_park_detail)
            detail_req.meta['ballpark'] = ballpark

            yield detail_req

    def parse_park_detail(self, response):
        table = response.css('div#content table.itable tr:nth-child(n+3)')

        for tr in table:
            bpe = copy.copy(response.meta['ballpark'])
            bpe['year'] = tr.xpath('./td[1]//a/text()').extract_first()
            bpe['capacity'] = tr.xpath('./td[3]//text()').extract_first()

            fd_fields = (
                # field dimensions
                'fd_lf', 'fd_slf', 'fd_lfa', 'fd_lcf', 'fd_lcc',
                'fd_cf', 'fd_rcc', 'fd_rcf', 'fd_rfa', 'fd_srf',
                'fd_rf',

                # wall heights
                'w_lf', 'w_lcf', 'w_cf', 'w_rcf', 'w_rf',

                # field area
                'fair_area', 'foul_area', 'backstop_area',
            )

            for i in range(4, len(fd_fields) + 4):
                fd_field = fd_fields[i - 4]
                value = tr.xpath('./td[{}]//text()'.format(i)).extract_first()
                if isinstance(value, str):
                    value = value.strip()
                bpe[fd_field] = value

            yield bpe
