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
    # time
    'век': {'shorteners': {'в': 0.1, 'в.': 0.6, 'век.': 0.3}, 'same_prob': 0.2, 'token': 'time_a'},
    'год': {'shorteners': {'г.': 0.7, 'г': 0.3}, 'same_prob': 0.2, 'token': 'time_b', 'exclusions': ['лет']},
    'месяц': {'shorteners': {'мес.': 0.7, 'мес': 0.3}, 'same_prob': 0.2, 'token': 'time_с'},
    'день': {'shorteners': {'д.': 0.7, 'д': 0.3}, 'same_prob': 0.2, 'token': 'time_d'},
    'час': {'shorteners': {'ч.': 0.7, 'ч': 0.3}, 'same_prob': 0.2, 'token': 'time_e'},
    'минута': {'shorteners': {'мин.': 0.7, 'мин': 0.3}, 'same_prob': 0.2, 'token': 'time_f'},
    'секунда': {'shorteners': {'сек.': 0.5, 'сек': 0.3, 'с.': 0.2}, 'same_prob': 0.2, 'token': 'time_g'},
    'неделя': {'shorteners': {'нед.': 0.7, 'нед': 0.3}, 'same_prob': 0.2, 'token': 'time_h'},
    'лет': {'shorteners': {'л.': 0.7, 'л': 0.3}, 'same_prob': 0.2, 'token': 'time_k', 'exact': True},
    # phys
    'ватт': {'shorteners': {'вт.': 0.2, 'вт': 0.2, 'Вт.': 0.2, 'Вт': 0.2, 'W': 0.2}, 'same_prob': 0.2, 'token': 'phys_а'},
    'киловатт': {'shorteners': {'квт.': 0.2, 'квт': 0.2, 'кВт.': 0.2, 'кВт': 0.2, 'kW': 0.2}, 'same_prob': 0.2, 'token': 'phys_b'},
    'мегаватт': {'shorteners': {'мвт.': 0.2, 'мвт': 0.2, 'мВт.': 0.2, 'мВт': 0.2, 'mW': 0.2}, 'same_prob': 0.2, 'token': 'phys_c'},
    'вольт': {'shorteners': {'в.': 0.2, 'в': 0.2, 'В.': 0.2, 'В': 0.2, 'V': 0.2}, 'same_prob': 0.2, 'token': 'phys_d'},
    'паскаль': {'shorteners': {'па.': 0.2, 'па': 0.2, 'Па.': 0.2, 'Па': 0.2, 'Pa': 0.2}, 'same_prob': 0.2, 'token': 'phys_e'},
    'градус': {'shorteners': {'гр.': 0.7, 'гр': 0.3}, 'same_prob': 0.2, 'token': 'phys_f'},
    # months
    'январь': {'shorteners': {'янв.': 0.7, 'янв': 0.3}, 'same_prob': 0.2, 'token': 'months_a'},
    'февраль': {'shorteners': {'фев.': 0.7, 'фев': 0.3}, 'same_prob': 0.2, 'token': 'months_b'},
    'март': {'shorteners': {'март.': 0.7, 'март': 0.3}, 'same_prob': 0.999, 'token': 'months_c'},
    'апрель': {'shorteners': {'апр.': 0.7, 'апр': 0.3}, 'same_prob': 0.2, 'token': 'months_d'},
    'май': {'shorteners': {'мая.': 0.7, 'мая': 0.3}, 'same_prob': 0.999, 'token': 'months_e'},
    'июнь': {'shorteners': {'июн.': 0.7, 'июн': 0.3}, 'same_prob': 0.2, 'token': 'months_f'},
    'июль': {'shorteners': {'июл.': 0.7, 'июл': 0.3}, 'same_prob': 0.2, 'token': 'months_g'},
    'август': {'shorteners': {'авг.': 0.7, 'авг': 0.3}, 'same_prob': 0.2, 'token': 'months_h'},
    'сентябрь': {'shorteners': {'сен.': 0.7, 'сен': 0.3}, 'same_prob': 0.2, 'token': 'months_k'},
    'октябрь': {'shorteners': {'сен.': 0.7, 'сен': 0.3}, 'same_prob': 0.2, 'token': 'months_l'},
    'ноябрь': {'shorteners': {'ноя.': 0.4, 'ноябр.': 0.3, 'ноя': 0.3}, 'same_prob': 0.2, 'token': 'months_m'},
    'декабрь': {'shorteners': {'дек.': 0.7, 'дек': 0.3}, 'same_prob': 0.2, 'token': 'months_n'},
    # currency
    'рубль': {'shorteners': {'руб.': 0.4, 'руб': 0.3, 'р.': 0.3}, 'same_prob': 0.2, 'token': 'cur_a'},
    'доллар': {'shorteners': {'дол.': 0.3, 'дол': 0.3, 'долл.': 0.1, '$': 0.3}, 'same_prob': 0.2, 'token': 'cur_b'},
    'евро': {'shorteners': {'евр.': 0.1, 'евр': 0.1, 'е.': 0.1, '€': 0.7}, 'same_prob': 0.4, 'token': 'cur_c'},
    'копейка': {'shorteners': {'коп.': 0.4, 'коп': 0.4, 'к.': 0.2}, 'same_prob': 0.2, 'token': 'cur_d'},
    # short
    'в том числе': {'shorteners': {'в т. ч.': 0.9, 'в том ч.': 0.1}, 'same_prob': 0.2, 'token': 'short_a', 'exact': True},
    'и так далее': {'shorteners': {'и т. д.': 0.2, 'итд.': 0.2, 'и т.д.': 0.2, 'итд': 0.2, 'и т д': 0.2}, 'same_prob': 0.2, 'token': 'short_b', 'exact': True},
    'и тому подобное': {'shorteners': {'и т. п.': 0.2, 'итп.': 0.2, 'и т.п.': 0.2, 'итп': 0.2, 'и т п': 0.2}, 'same_prob': 0.2, 'token': 'short_c', 'exact': True},
    'и другие': {'shorteners': {'и др.': 0.5, 'и др': 0.5}, 'same_prob': 0.2, 'token': 'short_d', 'exact': True},
    'и прочие': {'shorteners': {'и пр.': 0.5, 'и пр': 0.5}, 'same_prob': 0.2, 'token': 'short_e', 'exact': True},
    'кандидат технических наук': {'shorteners': {'к. т. н..': 0.9, 'к т н': 0.1}, 'same_prob': 0.2, 'token': 'short_f'},
    'кандидат медицинских наук': {'shorteners': {'к. м. н..': 0.9, 'к м н': 0.1}, 'same_prob': 0.2, 'token': 'short_g'},
}
REGVAR_TEMPLATE = '(?i)([\b|\W])({})([\b|\W])'


def get_shorteners_model():
    morph = pymorphy2.MorphAnalyzer()
    model = SHORTENERS_MODEL.copy()
    for term, inner_dict in model.items():

        if 'exclusions' in inner_dict:
            exclusions = inner_dict['exclusions']
        else:
            exclusions = []

        if 'exact' not in inner_dict:
            all_forms = set(
                [
                    w.word for w in morph.parse(term)[0].lexeme
                    if ('аббр' not in w.tag.cyr_repr) and ('СУЩ' in w.tag.cyr_repr) and (w.word.lower() not in exclusions)
                ]
            )
        else:
            all_forms = [term]

        regvar = REGVAR_TEMPLATE.format('|'.join(all_forms))
        model[term]['regvar'] = re.compile(regvar)

        ps = [v for k, v in model[term]['shorteners'].items()]
        assert sum(ps) == 1.

    return model
