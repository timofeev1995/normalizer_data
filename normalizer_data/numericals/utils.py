import re


def has_digits(text):
    if len(re.findall(r'\d+', text)) > 0:
        return True
    else:
        return False


def has_latin(text):
    if len(re.findall(r'[Aa-zZ]+', text)) > 0:
        return True
    else:
        return False


def valid_sentence(text):
    # TODO: добавить, чтобы случаи типа 10 млрд. не учитывались, иначе -> 10000000000 (а мы хотели бы "десять миллиардов")
    return not (has_digits(text) or has_latin(text))


def is_usual_case(sentence):
    pattern = r'\b10\b|\b100\b|\b1000\b|\b1\b|\b2\b|\b3\b'
    if len(re.findall(pattern, sentence)) > 0:
        return True
    else:
        return False


def numericalize_text(sentence, extractor):
    if valid_sentence(sentence):
        if len(extractor(sentence)) > 0:
            replaced = extractor.replace_groups(sentence)
            if not is_usual_case(replaced):
                return sentence, replaced
    return None
