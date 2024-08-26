from flask import session

import os
import json


def load_translations(lang):
    with open(os.path.join('translations', f'{lang}.json')) as f:
        return json.load(f)


def get_translations():
    lang = session.get('lang', 'en')
    print(lang)
    return load_translations(lang)
