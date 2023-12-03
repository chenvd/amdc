from jinja2 import Environment, FileSystemLoader
import os


def generate(meta, file_name, image_extension, save_path):
    env = Environment(loader=FileSystemLoader('./utils/'))
    template = env.get_template('nfo_template.xml')
    nfo = template.render(meta=meta, file_name=file_name, image_extension=image_extension)

    with open(os.path.join(save_path, f'{file_name}.nfo'), 'w') as f:
        f.write(nfo)
