#-*- coding:utf-8 -*-
import io
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
        url = u"https://cn.bing.com/dict/search?q={}".format(self.word)
        data = self.get_response(url)
        soup = parse_html(data)
        
        # <div class="qdef">
        element = soup.find('div', {'class': 'qdef'})
        if not element:
            # Save full page for debugging so we can inspect the actual DOM
            try:
                filename_full = 'dictionary_bing_full_{}.html'.format(_safe_filename_component(self.word))
                export_path_full = os.path.join(os.path.expanduser('~'), filename_full)
                with io.open(export_path_full, 'w', encoding='utf-8') as f:
                    f.write(str(soup))
                print('Bing: full page saved to {}'.format(export_path_full))
            except Exception as e:
                print('Bing: failed to save full page: {}'.format(e))
            raise ValueError('Bing: definition container not found: {}'.format(url))

        body_html = str(element)

        try:
            filename = 'dictionary_bing_{}.html'.format(_safe_filename_component(self.word))
            export_path = os.path.join(os.path.expanduser('~'), filename)
            with io.open(export_path, 'w', encoding='utf-8') as f:
                f.write(body_html)
        except Exception as e:
            print('Bing: export failed for {}: {}'.format(export_path, e))

        result = {
            'ee': body_html,
        }

        return self.cache_this(result)
    
    @export('DEF')
    def fld_definition(self):
        return self._get_field('ee')

# A dictionary “provider” (web services) inside this Anki add-on
# Exported field: fld_definition