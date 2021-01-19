import re
from typing import Dict

import numpy as np

from normalizer_data.numericals.extractor import NumberExtractor
from normalizer_data.numericals.utils import numericalize_text, has_digits
from normalizer_data.shorteners.shorteners_model import get_shorteners_model


def has_latin(text):
    if len(re.findall(r'[Aa-zZ]+', text)) > 0:
        return True
    else:
        return False


def build_sample(text: str, number_extractor: NumberExtractor, shortener_model: Dict):

    changes = 0
    if has_latin(text) or has_digits(text):
        return None

    for term, model in shortener_model.items():
        while True:
            found = re.search(model['regvar'], text)
            if found is not None:
                coin = np.random.rand()
                if coin > model['same_prob']:
                    text = text.replace(found.group(2), model['token'])
                else:
                    text = text.replace(found.group(2), found.group(2) + 'selftoken')
                changes += 1
            else:
                text = text.replace('selftoken', '')
                break

    num_result = numericalize_text(text, extractor=number_extractor)
    if num_result is not None:
        replaced, num_changes = num_result
    else:
        replaced, num_changes = text, 0

    if max(num_changes, changes) == 0:
        return None

    for term, model in shortener_model.items():
        replace_settings = [(k, v) for k, v in model['shorteners'].items()]
        replace_options = [x[0] for x in replace_settings]
        replace_probabilities = [x[1] for x in replace_settings]
        token = model['token']
        while True:
            if token not in replaced:
                break
            else:
                to_replace = np.random.choice(replace_options, p=replace_probabilities)
                replaced = replaced.replace(token, to_replace, 1)

    return replaced, num_changes, changes
