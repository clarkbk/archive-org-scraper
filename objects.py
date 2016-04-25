import os
import re
import requests

from bs4 import BeautifulSoup
from urlparse import urlparse
from utils import check_if_path_exists
from utils import get_background_url_from_tag
from utils import get_logger

logger = get_logger()


class Album:
    def __init__(self, url):
        self.url = url
        self.id = ''
        self.title = ''
        self.date = ''
        self.images = []
        self.set_id_from_url()
        self.set_images_and_metadata()

    def set_id_from_url(self):
        pattern = '\/([A-Za-z0-9]+)$'
        rgx = re.search(pattern, self.url)
        self.id = rgx.group(1)

    def set_images_and_metadata(self):
        url = 'http://web.archive.org{0}'.format(self.url)
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        # set title
        header = soup.find('div', {'class': 'header'})
        self.title = header.h1.get_text()

        # set date
        meta_info = soup.find('ul', {'class': 'meta-info'})
        self.date = meta_info.find_all('li')[-1].get_text() \
            .replace('Album created: ', '')

        # set images
        tags = soup.find_all('a', {'class': 'thumb'})
        for tag in tags:
            thumb_url = get_background_url_from_tag(tag)
            image = Image(thumb_url)
            self.images.append(image)
        logger.info('added {0} photos to album "{1}"'
                    .format(len(self.images), self.title))

    def save_images(self):
        """For each Image associated with an Album, make a web request and save it
        to a local directory"""
        folder = 'output/{0}'.format(self.id)
        infofile = '{0}/album-info.txt'.format(folder)
        check_if_path_exists(infofile)
        with open(infofile, 'wb') as f:
            f.write('{title}\n{count}\n{date}\n{url}'.format(
                title=self.title,
                count='{0} photos'.format(len(self.images)),
                date=self.date,
                url='http://web.archive.org{0}'.format(self.url),
            ))
        for image in self.images:
            r = requests.get('http://web.archive.org{0}'.format(image.url))
            if r.status_code != 200:
                continue
            with open('{0}/{1}'.format(folder, image.filename), 'wb') as f:
                for chunk in r:
                    f.write(chunk)


class Image:
    def __init__(self, thumb_url):
        self.thumb_url = thumb_url
        self.set_url_from_thumb()
        self.filename = os.path.split(urlparse(self.url).path)[-1]

    def set_url_from_thumb(self):
        pattern = '/web/(?:[a-z0-9_]+)/http://thumb\d+?.webshots.net/t/' \
            '(\d+)([\/A-Za-z0-9]+)_th.jpg'
        rgx = re.search(pattern, self.thumb_url)
        extract = (rgx.group(1), rgx.group(2))
        url = '/web/20121108151015im_/' \
            'http:/image{0}.webshots.com/{1}_ph.jpg'
        self.url = url.format(*extract)
