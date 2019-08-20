import os
from jinja2 import Environment, PackageLoader

app_name = 'deckgl'
env = Environment(
    loader=PackageLoader(app_name, '/templates'),
)

def format(deckgl_layer, **kwargs):
    template = env.get_template('{}.html'.format(deckgl_layer))
    return template.render(**kwargs)