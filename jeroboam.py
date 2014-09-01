#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# stdlib
import configparser
from logging.handlers import RotatingFileHandler
import logging
import mimetypes
import os
import subprocess
import sys

# create virtualenv before importing pipped package
VENV_PATH = os.path.join(os.getcwd(), 'venv')
VENV_PYTHON = os.path.join(VENV_PATH, 'bin', 'python')
VENV_PIP = os.path.join(VENV_PATH, 'bin', 'pip')
PACKAGES = ['bottle', 'pillow']  # + watchdog to update cache on-the-fly
PACKAGES += ['ipdb']  # dev packages

if not os.path.exists(VENV_PIP):
    print("Create virtual environment, this should happen only once.")
    subprocess.call(['pyvenv', VENV_PATH])  # needs pyvenv in PATH
    subprocess.call([VENV_PIP, '--quiet', 'install'] + PACKAGES)

if not VENV_PYTHON == sys.executable:
    subprocess.call([VENV_PYTHON, os.path.realpath(__file__)])
    sys.exit(0)  # to stop here the wrong environment


## Now begins the code using virtual environment
from PIL import Image
#import bottle
# constants
APP_NAME = 'jeroboam'
CONFIG_FILE = 'config.ini'
CACHE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache')
THUMBNAIL_SIZE = '150'  # default


class Jeroboam:
    def __init__(self, logger):
        self.config = configparser.ConfigParser()
        self.log = logger
        self.tree = []

    def init(self):
        self.get_config()
        self.create_cache()

    def get_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.log.info("Config file does not exist, ask user to create one.")
            self.create_config()
        else:
            self.config.read(CONFIG_FILE)
            # check config integrity
            if not os.path.exists(self.config['DEFAULT']['directory']):
                self.log.error("Picture directory do not exist. You need one to use Jeroboam.")
                sys.exit(1)

    def create_config(self):
        directory = input("Please, specify the directory where your pictures are: ")
        self.config['DEFAULT']['directory'] = directory
        self.config['DEFAULT']['thumbnail_size'] = THUMBNAIL_SIZE

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def create_cache(self):
        if os.path.exists(CACHE_DIR) and os.path.isdir(CACHE_DIR):
            self.log.info("Read and update cache.")
        else:
            os.mkdir(CACHE_DIR)
            self.log.info("Creating cache directories.")

        nb_files = 0
        nb_cache_files = 0
        for subdir, dirs, files in os.walk(self.config['DEFAULT']['directory']):
            # recreate dirs
            cache_dir = None
            if subdir.startswith(self.config['DEFAULT']['directory']):
                length = len(self.config['DEFAULT']['directory']) + 1
                self.tree.append(subdir[length:])
                cache_dir = os.path.join(CACHE_DIR, subdir[length:])
                if not os.path.exists(cache_dir):
                    os.mkdir(cache_dir)
                    self.log.info("Creating cache dir: " + cache_dir)

            # recreate thumbnails
            for file in files:
                path = os.path.join(subdir, file)
                cache_path = os.path.join(cache_dir, file)
                mimetype = mimetypes.guess_type(file)
                if mimetype and not os.path.exists(cache_path):
                    filetype = mimetype[0].split('/')[0]
                    if filetype == 'image':
                        self.log.info("Caching: " + cache_path)
                        im = Image.open(path)
                        size = (int(self.config['DEFAULT']['thumbnail_size']),
                                int(self.config['DEFAULT']['thumbnail_size']))
                        im.thumbnail(size, Image.BICUBIC)
                        im.save(cache_path, im.format)
                        nb_cache_files += 1
                nb_files += 1

        self.log.info(str(nb_files) + " files found - " + str(nb_cache_files) + " files cached")

    def run_bottle(self):
        from bottle import route, run, static_file, view

        @route('/:path#.*#')
        @view('theme')
        def index(path):
            pic_path = os.path.join(CACHE_DIR, path)
            if os.path.isdir(pic_path):
                return dict(tree=self.tree)
            else:
                full_path = os.path.join(self.config['DEFAULT']['directory'], path)
                return static_file(os.path.basename(pic_path), root=os.path.dirname(full_path))

        subprocess.Popen(['open', 'http://127.0.0.1:8080/'])
        run(debug=True)


def log():
    """ The app logger """
    logger = logging.getLogger(APP_NAME)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
    file_handler = RotatingFileHandler('/tmp/' + APP_NAME + '.log', 'a', 1000000, 1)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def main():
    """ Main function. """
    jeroboam = Jeroboam(log())
    jeroboam.init()
    jeroboam.run_bottle()


if __name__ == "__main__":
    main()
