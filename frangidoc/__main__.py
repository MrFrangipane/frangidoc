import argparse
import frangidoc


def process_args():
    parser = argparse.ArgumentParser(
        prog="frangidoc",
        description="Frangi Doc - Markdown from sources"
    )
    parser.add_argument(
        'module',
        type=str,
        help="Module to generate doc from, must be importable"
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help="Output filepath, optional (.md file is created next to module if not specified)"
    )
    parse_args = parser.parse_args()
    return parse_args


if __name__ == '__main__':
    args = process_args()
    frangidoc.generate_and_save(args.module, args.output)
