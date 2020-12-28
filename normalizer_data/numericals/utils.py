import re


def has_digits(text):
    if len(re.findall(r'\d+', text)) > 0:
        return True
    else:
        return False


def is_usual_case(sentence):
    pattern = r'\b10\b|\b100\b|\b1\b|\b2\b|\b3\b'
    if len(re.findall(pattern, sentence)) > 0:
        return True
    else:
        return False


def numericalize_text(sentence, extractor):
    len_matches = len(extractor(sentence))
    if len_matches > 0:
        replaced = extractor.replace_groups(sentence)
        if not is_usual_case(replaced):
            return replaced, len_matches

    return None
