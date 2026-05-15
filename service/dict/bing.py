#-*- coding:utf-8 -*-
from ..base import *

@register([u'Bing', u'Bing'])
class Bing(WebService):

    def __init__(self):
        super(Bing, self).__init__()

    def _get_from_api(self):
        data = self.get_response(u"http://cn.bing.com/dict/search?q={}".format(self.quote_word))
        soup = parse_html(data)
        result = {
            'def': [],
        }

        element = soup.find('div', class_='qdef')
        if element:
            element = getattr(element, 'ul', '')
            if element:
                result['def'] = u''.join([str(content) for content in element.contents])

        return self.cache_this(result)

    @with_styles(css='.pos{font-weight:bold;margin-right:4px;}', need_wrap_css=True, wrap_class='bing')
    def _css(self, val):
        return val
    
    @export('DEF')
    def fld_definition(self):
        val = self._get_field('def')
        if val == None or val == '':
            return ''
        return self._css(val)
