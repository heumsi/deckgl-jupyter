import os
from jinja2 import Environment, FileSystemLoader

current_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.join(current_dir, 'templates')

loader = FileSystemLoader(searchpath=path)
env = Environment(loader=loader)

def format(template_name, **kwargs):
    template = env.get_template('{}.html'.format(template_name))
    return template.render(**kwargs)