#-*- coding:utf-8 -*-
import os
import re

from ..base import *


def _safe_filename_component(value: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', value).strip('_')


@register([u'Bing', u'Bing'])
class Bing(WebService):

    def __init__(self):
        super(Bing, self).__init__()

    def _get_from_api(self):
        url = u"https://cn.bing.com/dict/search?q={}".format(self.quote_word)
        data = self.get_response(url)
        soup = parse_html(data)
        
        element = soup.find('div', class_='qdef')
        if not element:
            raise ValueError('Bing: definition container not found: {}'.format(url))
        
        body_html = str(element)

        try:
            filename = 'dictionary_bing_{}.html'.format(_safe_filename_component(self.quote_word))
            export_path = os.path.join(os.path.expanduser('~'), filename)
            with open(export_path, 'w', encoding='utf-8') as f:
                f.write(body_html)
        except Exception:
            pass

        result = {
            'ee': body_html,
        }

        return self.cache_this(result)
    
    @export('DEF')
    def fld_definition(self):
        return self._get_field('ee')

# A dictionary “provider” (web services) inside this Anki add-on
# Exported field: fld_definition