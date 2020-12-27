from pathlib import Path

from setuptools import find_packages, setup

THIS_DIR = Path(__file__).parent


def get_version(filename):
    from re import findall
    with open(filename) as f:
        metadata = dict(findall("__([a-z]+)__ = '([^']+)'", f.read()))
    return metadata['version']


def _get_requirements():
    with (THIS_DIR / 'requirements.txt').open() as fp:
        return fp.read()


setup(
    name='tts_imputer',
    version=get_version('normalizer_data/__init__.py'),
    description='Package to prepare datasets for further normalization task',
    packages=find_packages(exclude=['test', 'test.*']),
    install_requires=_get_requirements(),
    package_dir={'normalizer_data': 'normalizer_data'},
)
