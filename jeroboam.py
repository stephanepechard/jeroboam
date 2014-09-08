#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# stdlib
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
    try:
        subprocess.call(['pyvenv', VENV_PATH])  # needs pyvenv in PATH
    except FileNotFoundError:
        subprocess.call(['virtualenv', VENV_PATH])  # needs virtualenv in PATH
    subprocess.call([VENV_PIP, '--quiet', 'install'] + PACKAGES)

if not VENV_PYTHON == sys.executable:
    subprocess.call([VENV_PYTHON, os.path.realpath(__file__)])
    sys.exit(0)  # to stop here the wrong environment


## Now begins the code using virtual environment
try:
    import configparser  # python3
except ImportError:
    import ConfigParser as configparser  # python2
try:
   input = raw_input  # python2
except NameError:
   pass  # python3
from PIL import Image
# constants
APP_NAME = 'jeroboam'
CONFIG_FILE = 'config.ini'
CACHE_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cache')
THUMBNAIL_SIZE = '150'  # default
SUPPORTED_EXTENSIONS = ['gif', 'jpg', 'jpeg', 'png']

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
            if not os.path.exists(self.config.get('DEFAULT', 'directory')):
                self.log.error("Picture directory do not exist. You need one to use Jeroboam.")
                sys.exit(1)

    def create_config(self):
        directory = input("Please, specify the directory where your pictures are: ")
        self.config.set('DEFAULT', 'directory', directory)
        self.config.set('DEFAULT', 'thumbnail_size', THUMBNAIL_SIZE)

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)

    def create_cache(self):
        if os.path.exists(CACHE_DIR) and os.path.isdir(CACHE_DIR):
            self.log.info("Read and update cache.")
        else:
            os.mkdir(CACHE_DIR)
            self.log.info("Creating cache directories.")

        size = (int(self.config.get('DEFAULT', 'thumbnail_size')),
                int(int(self.config.get('DEFAULT', 'thumbnail_size')) * 1.618))
        for subdir, dirs, files in os.walk(self.config.get('DEFAULT', 'directory')):
            # recreate dirs
            length = len(self.config.get('DEFAULT', 'directory')) + 1
            path = subdir[length:]
            cache_dir = os.path.join(CACHE_DIR, path)
            if not os.path.exists(cache_dir):
                os.mkdir(cache_dir)
                self.log.info("Creating cache dir: " + cache_dir)

            # recreate thumbnails
            nb_files = 0
            for file in files:
                if file.split('.')[-1].lower() in SUPPORTED_EXTENSIONS:
                    nb_files += 1
                    cache_file = os.path.join(cache_dir, file)
                    if not os.path.exists(cache_file):
                        try:
                            im = Image.open(os.path.join(subdir, file))
                            im.thumbnail(size)
                            im.save(cache_file, im.format)
                            nb_files += 1
                        except IOError:
                            self.log.info('Error while opening: ' + os.path.join(subdir, file))

            # show directory only if supported files in it
            if nb_files:
                self.tree.append(path)

    def run_bottle(self):
        from bottle import route, run, static_file, view

        @route('/imagelightbox.min.js')
        def imagelightbox():
            return static_file('imagelightbox.min.js', root=os.path.dirname(__file__))

        @route('/cache/:path#.*#')
        def cache(path):
            pic_path = os.path.join(CACHE_DIR, path)
            if not os.path.isdir(pic_path):
                full_path = os.path.join(CACHE_DIR, path)
                return static_file(os.path.basename(pic_path), root=os.path.dirname(full_path))

        @route('/:path#.*#')
        @view('theme')
        def index(path):
            pic_path = os.path.join(CACHE_DIR, path)
            if os.path.isdir(pic_path):
                pictures = [os.path.join(path, pic) for pic in os.listdir(pic_path) if os.path.isfile(os.path.join(pic_path, pic))]
                return dict(tree=self.tree, pictures=pictures)
            else:
                full_path = os.path.join(self.config.get('DEFAULT', 'directory'), path)
                return static_file(os.path.basename(pic_path), root=os.path.dirname(full_path))

        subprocess.Popen(['open', 'http://0.0.0.0:8080'])
        run(host='0.0.0.0', debug=True)


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
