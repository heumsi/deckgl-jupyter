import os
from jinja2 import Environment, PackageLoader, FileSystemLoader

app_name = 'deckgl_jupyter'
env = Environment(
    #loader=PackageLoader(app_name, 'templates'),
    loader=FileSystemLoader('%s/templates/' %app_name)
)

def format(deckgl_layer, **kwargs):
    template = env.get_template('{}.html'.format(deckgl_layer))
    return template.render(**kwargs)