# -*- coding:utf-8 -*-

from ..base import *
from ...utils.misc import format_multi_query_word


@register([u'朗文', u'Longman'])
class Longman(WebService):

    def __init__(self):
        super(Longman, self).__init__()

    def _get_from_api(self):
        url = 'https://www.ldoceonline.com/dictionary/{}'.format(format_multi_query_word(self.quote_word))
        data = self.get_response(url)
        soup = parse_html(data)
        dictionary_div = soup.find('div', {'class': 'dictionary'})
        if not dictionary_div:
            raise ValueError('Longman: dictionary container not found: {}'.format(url))
        body_html = str(dictionary_div)

        word_info = {'ee': body_html}
        return self.cache_this(word_info)

    @export('DEF')
    @with_styles(cssfile='_longman.css')
    def fld_ee(self):
        return self._get_field('ee')
