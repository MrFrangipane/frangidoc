import sys
import logging
import argparse
from frangidoc import api


USAGE = """frangidoc <command> [<args>]
- git <repo_url> <output_dir>
"""


class FrangiDoc(object):
    def __init__(self):
        parser = argparse.ArgumentParser(
            prog="FrangiDoc",
            description="Generate markdown from reST-based docstrings",
            usage=USAGE
        )

        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print("Unrecognized command")
            parser.print_help()
            exit(1)

        callable_ = getattr(self, args.command)
        callable_()

    def git(self):
        parser = argparse.ArgumentParser(
            prog="frangidoc git",
            description='Generates Markdown from given Git repo url (repo must contain .frangidoc.yml config file)'
        )
        parser.add_argument(
            'url',
            type=str,
            help="Url of the git repository"
        )
        parser.add_argument(
            'output',
            type=str,
            help="Output directory"
        )
        parser.add_argument(
            '-i', '--include-images',
            action='store_true'
        )

        args = parser.parse_args(sys.argv[2:])
        api.clone_and_generate(args.url, args.output, include_images=args.include_images)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="%(message)s")
    FrangiDoc()
