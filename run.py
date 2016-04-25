import os
import requests

from bs4 import BeautifulSoup
from objects import Album


def get_albums_from_user(user):
    """Given the URL of a Webshots user's profile page on archive.org,
    return a list of albums"""
    albums = []
    host = 'http://web.archive.org'
    url = '{0}/web/20121108151000/http://community.webshots.com/user/{1}' \
        .format(host, user)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    lis = soup.find_all('li', {'class': 'album'})
    for li in lis:
        a = li.h4.a
        album = Album(a.get('href'))
        albums.append(album)
    return albums

if __name__ == '__main__':
    user = os.environ['WEBSHOTS_USER']
    albums = get_albums_from_user(user)
    for album in albums:
        album.save_images()
