import logging
from frangidoc.parser import parse_module
from frangidoc.renderer import render


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    filepath = 'R:/users/v.moriceau/blender-lab/libs/nomenclature/texture_filepath.py'

    logging.info('parsing ' + filepath)

    module = parse_module(filepath)
    page = render(module)

    logging.info('done !')

    print(page)
