import errno
import logging
import os
import re


def get_logger():
    logger = logging.getLogger('app')
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    pattern = '%(asctime)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(pattern)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger


def get_background_url_from_tag(tag):
    css = tag.get('style')
    pattern = 'background-image: url\((.+)\)'
    rgx = re.search(pattern, css)
    return rgx.group(1)


def check_if_path_exists(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
