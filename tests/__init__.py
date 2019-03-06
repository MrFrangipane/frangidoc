from frangidoc.parser import parse_module
from frangidoc.renderer import render


if __name__ == '__main__':
    module = parse_module('R:/users/v.moriceau/blender-lab/libs/nomenclature/texture_filepath.py')
    page = render(module)

    print(page)
