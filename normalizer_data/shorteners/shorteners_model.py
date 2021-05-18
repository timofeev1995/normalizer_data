import re
from string import ascii_letters
from pathlib import Path

import numpy as np
import pymorphy2
import yaml

SHORTENERS_MODEL_PATH = Path(__file__).parent.absolute() / 'model.yaml'
REGVAR_TEMPLATE = '(?i)([\b|\W])({})([\b|\W])'
SAME_PROB = 0.2


def get_shorteners_model():
    morph = pymorphy2.MorphAnalyzer()
    shorteners_model = {}

    with open(SHORTENERS_MODEL_PATH, 'r') as file:
        model_raw = file.read()
    model = yaml.load(model_raw)

    for group_name, this_model in model.items():
        for item_num, (term, inner_dict) in enumerate(this_model.items()):

            same_prob = inner_dict.get('same_prob', SAME_PROB)
            if 'exclusions' in inner_dict:
                exclusions = inner_dict['exclusions']
            else:
                exclusions = []

            if not inner_dict.get('exact', False):
                all_forms = set(
                    [
                        w.word for w in morph.parse(term)[0].lexeme
                        if ('аббр' not in w.tag.cyr_repr)
                           and ('СУЩ' in w.tag.cyr_repr)
                           and (w.word.lower() not in exclusions)
                    ]
                )
                if len(all_forms) == 0:
                    all_forms = [term]
            else:
                all_forms = [term]

            regvar = REGVAR_TEMPLATE.format('|'.join(all_forms))

            occurrence_map = {
                'regvar': re.compile(regvar),
                'same_prob': same_prob,
                'shorteners': inner_dict['shorteners'],
                'token': group_name + '_' + ascii_letters[item_num]
            }
            ps = [v for k, v in occurrence_map['shorteners'].items()]
            assert np.isclose(sum(ps), 1.)
            assert len(all_forms) > 0

            shorteners_model[term] = occurrence_map

    return shorteners_model
