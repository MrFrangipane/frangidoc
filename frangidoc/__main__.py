import argparse
import frangidoc


def process_args():
    parser = argparse.ArgumentParser(description="Frangi doc - Markdown from sources")
    parser.add_argument(
        '-m',
        '--module-name',
        type=str,
        help="Module to generate doc from, must be importable"
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        help="Output filepath"
    )
    parse_args = parser.parse_args()
    return parse_args


if __name__ == '__main__':
    args = process_args()

    if args.module_name and args.output:
        frangidoc.generate_and_save(args.module_name, args.output)
