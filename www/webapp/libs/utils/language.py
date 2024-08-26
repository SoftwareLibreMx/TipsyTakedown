from flask import session

import os
import json

TRANSLATIONS = None
# default language
LANG = 'en'


def load_translations(lang):
    with open(os.path.join('translations', f'{lang}.json')) as f:
        return json.load(f)


def get_translations(page=None):
    global TRANSLATIONS, LANG
    lang = session.get('lang', LANG)
    if TRANSLATIONS is None or lang != LANG:
        TRANSLATIONS = load_translations(lang)
    if page:
        return {
            page: TRANSLATIONS[page],
            'navbar': TRANSLATIONS['navbar']
        }
    else:
        return {'navbar': TRANSLATIONS['navbar']}
