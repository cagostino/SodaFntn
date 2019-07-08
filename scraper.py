from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from multiprocessing.pool import ThreadPool
import requests
import os


global BASE
BASE = "http://freemidi.org"


def cook_soup(url):
    html = requests.get(url).content
    return BeautifulSoup(html, "html.parser")


def get_genre_artists(genre):
    url = BASE + "/genre-" + str(genre)
    soup = cook_soup(url)
    bands = soup.find_all("div", attrs={"class": "genre-band-container"})
    print("fetching artists", "for", genre, "...")
    return [BASE + "/" + band.div.a["href"] for band in bands]


def get_artist_songs(url):
    soup = cook_soup(url)
    songs = soup.find_all("div", attrs={"itemprop": "tracks"})
    return [
        (song.span.a.text.strip("\n"), BASE + "/" + song.span.a["href"])
        for song in songs
    ]


class Scraper:
    fetch_pool = ThreadPool(10)
    download_pool = ThreadPool(10)

    def __init__(self, genres=[]):
        self.genres = genres

    def download(self):
        for genre in self.genres:
            genre_path = os.path.realpath(".") + "/midi/" + str(genre)
        try:
            os.makedirs(genre_path)
        except FileExistsError:
            pass
        os.chdir(genre_path)

        artists = get_genre_artists(genre)
        artists_songs = self.fetch_pool.imap_unordered(get_artist_songs, artists)
        for songs in tqdm(artists_songs):
            self.download_pool.imap(
                lambda x: urlretrieve(x[1], str(x[0]) + ".mid"), songs
            )


if __name__ == "__main__":
    genres = ["pop"]
    Scraper(genres).download()
