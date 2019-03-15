import logging
import frangidoc


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)

    frangidoc.clone_and_generate('http://gitlab.cubedns.fr/cube/tube.git', 'D:/frangidoc/')
    logging.info('done !')
