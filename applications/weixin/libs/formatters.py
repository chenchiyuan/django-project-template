# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import bleach
from bs4 import BeautifulSoup
from applications.weixin.tasks import replace_image


class BasicFormatter(object):
    @classmethod
    def format(cls, html, **kwargs):
        cleaned_html = BlenchHtml.clean_html(html)
        soup = BeautifulSoup(cleaned_html)
        formatted_soup = cls.format_stack(soup, **kwargs)
        return str(formatted_soup)

    @classmethod
    def format_stack(cls, soup, **kwargs):
        soup = cls.format_image(soup, **kwargs)
        soup = cls.format_table(soup)
        return soup

    @classmethod
    def format_image(cls, soup, **kwargs):
        images = soup.find_all('img')
        for image in images:
            image['class'] = "img-responsive"
            image['src'] = replace_image(image['src'], **kwargs)
        return soup

    @classmethod
    def format_table(cls, soup):
        tables = soup.find_all("table")
        for table in tables:
            table['class'] = "table table-bordered"
        return soup


class BlenchHtml(object):
    @classmethod
    def clean_html(cls, html):
        validate_tags = ['p', 'br', 'span', 'strong', 'tbody', 'td', 'tr',
                     'a', 'b', 'strong', 'font', 'h1', 'h2', 'h3',
                     'h4', 'h5', 'h6', 'img', 'table']

        validate_attrs = {
            '*': ['style'],
            'a': ['href', 'rel'],
            'p': ['style'],
            'tr': ['style'],
            'td': ['style', 'rowspan', 'colspan'],
            'font': ['color', ],
            'img': ['src', 'alt']
        }

        validate_styles = [
            'color', 'font-weight', 'font-family', 'background-color',
        ]

        cleaned_html = bleach.clean(html, tags=validate_tags,
        attributes=validate_attrs, styles=validate_styles, strip=True)
        return cleaned_html