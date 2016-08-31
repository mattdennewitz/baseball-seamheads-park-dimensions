# -*- coding: utf-8 -*-

import scrapy


class Ballpark(scrapy.Item):
    name = scrapy.Field()
    location = scrapy.Field()
    year = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    altitude = scrapy.Field()
    capacity = scrapy.Field()

    # field dimensions
    fd_lf = scrapy.Field()
    fd_slf = scrapy.Field()
    fd_lfa = scrapy.Field()
    fd_lcf = scrapy.Field()
    fd_lcc = scrapy.Field()
    fd_cf = scrapy.Field()
    fd_rcc = scrapy.Field()
    fd_rcf = scrapy.Field()
    fd_rfa = scrapy.Field()
    fd_srf = scrapy.Field()
    fd_rf = scrapy.Field()

    # wall height
    w_lf = scrapy.Field()
    w_lcf = scrapy.Field()
    w_cf = scrapy.Field()
    w_rcf = scrapy.Field()
    w_rf = scrapy.Field()

    fair_area = scrapy.Field()
    foul_area = scrapy.Field()
    backstop_area = scrapy.Field()
