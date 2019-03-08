import logging
from frangidoc.parser import parse_module
from frangidoc.renderer import render_summary


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    filepath = 'R:/users/v.moriceau/tube/api/python/tubepyside.py'

    logging.info('parsing ' + filepath)

    module = parse_module(filepath)
    page = render_summary(module)

    logging.info('done !')

    print(page)
