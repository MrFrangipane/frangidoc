import sys
import logging
import frangidoc


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    frangidoc.clone_and_generate(sys.argv[1], '/tmp/frangidoc/')
    logging.info('done !')
