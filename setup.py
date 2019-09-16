from setuptools import setup, find_packages

setup(
    name                = 'deckgljupyter',
    version             = '0.1.1.2',
    license             = 'MIT',
    description         = 'Let deck.gl be created in jupyter notebook.',
    long_description    = open('readme.md').read(),
    long_description_content_type = 'text/markdown',
    author              = 'heumsi',
    author_email        = 'heumsi@naver.com',
    url                 = 'https://github.com/heumsi/deckgl-jupyter',
    download_url        = 'https://github.com/heumsi/deckgl-jupyter/archive/master.zip',
    install_requires    =  ['mapboxgl', 'jinja2', ],
    packages            = find_packages(exclude = []),
    keywords            = ['deckgl', 'mapboxgl', 'location data', 'visualization'],
    python_requires     = '>=3',
    package_data        = {},
    zip_safe            = False,
    classifiers         = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
)
