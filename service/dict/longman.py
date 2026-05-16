# -*- coding:utf-8 -*-

import io
import os
import re

from ..base import *
from ...utils.misc import format_multi_query_word


def _safe_filename_component(value: str) -> str:
    # Keep it simple & cross-platform: letters/numbers/._- only.
    return re.sub(r'[^A-Za-z0-9._-]+', '_', value).strip('_')


@register([u'朗文', u'Longman'])
class Longman(WebService):

    def __init__(self):
        super(Longman, self).__init__()

    def _get_from_api(self):
        url = 'https://www.ldoceonline.com/dictionary/{}'.format(format_multi_query_word(self.quote_word))
        data = self.get_response(url)
        soup = parse_html(data)
        dictionary_div = soup.find('div', {'class': 'dictionary'})
        # <div class="dictionary">
        if not dictionary_div:
            raise ValueError('Longman: dictionary container not found: {}'.format(url))
        body_html = str(dictionary_div)

        try:
            dictionary_quote_word = format_multi_query_word(self.word)
            filename = 'dictionary_longman_{}.html'.format(_safe_filename_component(dictionary_quote_word))
            export_path = os.path.join(os.path.expanduser('~'), filename)
            with io.open(export_path, 'w', encoding='utf-8') as f:
                f.write(body_html)
        except Exception as e:
            print('Longman: export failed for {}: {}'.format(export_path, e))

        word_info = {'ee': body_html}
        return self.cache_this(word_info)

    @export('DEF')
    def fld_ee(self):
        return self._get_field('ee')

# A dictionary “provider” (web services) inside this Anki add-on
# Exported field: fld_ee 