import sys
import logging
import argparse
import api


USAGE = """frangidoc <command> [<args>]
- module <module_name>
- git <repo_url>
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

    def module(self):
        parser = argparse.ArgumentParser(
            prog="frangidoc module",
            description='Generates Markdown from given module name (must be importable)'
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
            help="Specify output file (same as module if not specified)"
        )
        args = parser.parse_args(sys.argv[2:])

        api.generate_and_save(args.module, args.output)

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
        args = parser.parse_args(sys.argv[2:])

        api.clone_and_generate(args.url, args.output)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    FrangiDoc()
