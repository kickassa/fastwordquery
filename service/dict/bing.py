#-*- coding:utf-8 -*-
from ..base import *

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
        
        result = {
            'ee': str(element),
        }

        return self.cache_this(result)
    
    @export('DEF')
    def fld_definition(self):
        return self._get_field('ee')

# A dictionary “provider” (web services) inside this Anki add-on
# Exported field: fld_definition