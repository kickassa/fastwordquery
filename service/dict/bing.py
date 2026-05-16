#-*- coding:utf-8 -*-
from ..base import *

@register([u'Bing', u'Bing'])
class Bing(WebService):

    def __init__(self):
        super(Bing, self).__init__()

    def _get_from_api(self):
        data = self.get_response(u"https://cn.bing.com/dict/search?q={}".format(self.quote_word))
        soup = parse_html(data)
        result = {
            'def': u'',
        }

        element = soup.find('div', class_='qdef')
        if element:
            result['def'] = str(element)

        return self.cache_this(result)
    
    @export('DEF')
    def fld_definition(self):
        return self._get_field('def') or ''

# A dictionary “provider” (web services) inside this Anki add-on
# Exported field: fld_definition