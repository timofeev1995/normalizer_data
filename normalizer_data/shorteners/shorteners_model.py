import re

import pymorphy2

SHORTENERS_MODEL = {
    # numericals
    'тысяча': {'shorteners': {'тыс': 0.4, 'т.': 0.2, 'тыс.': 0.4}, 'same_prob': 0.2, 'token': 'num_a'},
    'миллион': {'shorteners': {'млн': 0.5, 'млн.': 0.5}, 'same_prob': 0.2, 'token': 'num_b'},
    'миллиард': {'shorteners': {'млрд': 0.5, 'млрд.': 0.5}, 'same_prob': 0.2, 'token': 'num_c'},
    # length
    'миллиметр': {'shorteners': {'мм': 0.5, 'мм.': 0.5}, 'same_prob': 0.2, 'token': 'len_a'},
    'сантиметр': {'shorteners': {'см': 0.5, 'см.': 0.5}, 'same_prob': 0.2, 'token': 'len_b'},
    'метр': {'shorteners': {'м': 0.5, 'м.': 0.5}, 'same_prob': 0.2, 'token': 'len_c'},
    'километр': {'shorteners': {'км': 0.5, 'км.': 0.5}, 'same_prob': 0.2, 'token': 'len_d'},
    # volume
    'миллилитр': {'shorteners': {'мл': 0.5, 'мл.': 0.5}, 'same_prob': 0.2, 'token': 'vol_a'},
    'литр': {'shorteners': {'л': 0.5, 'л.': 0.5}, 'same_prob': 0.2, 'token': 'vol_b'},
    # space
    'гектар': {'shorteners': {'га': 0.3, 'га.': 0.7}, 'same_prob': 0.2, 'token': 'square_a'},
}
REGVAR_TEMPLATE = '(?i)([\b|\W])({})([\b|\W])'


def get_shorteners_model():
    morph = pymorphy2.MorphAnalyzer()
    model = SHORTENERS_MODEL.copy()
    for term, inner_dict in model.items():
        all_forms = set(
            [
                w.word for w in morph.parse(term)[0].lexeme
                if ('аббр' not in w.tag.cyr_repr) and ('СУЩ' in w.tag.cyr_repr)
            ]
        )
        regvar = REGVAR_TEMPLATE.format('|'.join(all_forms))
        model[term]['regvar'] = re.compile(regvar)

    return model
