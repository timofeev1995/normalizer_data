from pathlib import Path

import pytest

import normalizer_data
from normalizer_data.numericals.extractor import NumberExtractor

EXAMPLES_PATH = Path(normalizer_data.__file__).parents[1] / 'test' / 'test_data' / 'replace_numbers_data.csv'
with open(EXAMPLES_PATH, 'r') as datafile:
    test_lines = [x.split('<sep>') for x in datafile.readlines()]
    TEST_EXAMPLES = [(x[0].strip(), x[1].strip()) for x in test_lines]

EXTRACTOR = NumberExtractor()


@pytest.mark.parametrize(['original', 'replaced'], TEST_EXAMPLES)
def test_replace_numbers(original, replaced):
    result = EXTRACTOR.replace_groups(original)
    assert result == replaced
