import os
from jinja2 import Environment, FileSystemLoader

# os.path.abspath(".")
loader = FileSystemLoader(searchpath="./templates/")
env = Environment(loader=loader, extensions=['jinja2.ext.do'])

def format(template_name, **kwargs):
    template = env.get_template('{}.html'.format(template_name))
    return template.render(**kwargs)