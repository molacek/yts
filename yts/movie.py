from flask import Blueprint, render_template
import requests
from bs4 import BeautifulSoup

bp = Blueprint('movie', __name__, url_prefix='/movie')


@bp.route('/<movie_id>', methods=('GET',))
def detail(movie_id):
    req = requests.get("https://yts.am/movie/{0:s}".format(movie_id))
    soup = BeautifulSoup(req.text, "html.parser")
    movie_info = soup.find(id="movie-info")
    movie_details = movie_info.find_all('div', class_='hidden-xs')[0]
    movie_title = movie_details.find('h1')
    movie_year = movie_details.find_all('h2')[0]
    movie_genre = movie_details.find_all('h2')[1]
    movie_thumbnail = soup.find_all('img', class_='img-responsive')[0]
    movie_synopsis = soup.find(id='synopsis')
    movie_synopsis = movie_synopsis.find_all('p')[0]
    bottom_info = soup.find_all('div', class_="bottom-info")[0]
    download = bottom_info.find_all('p', class_='hidden-md hidden-lg')[0]
    download = download.find_all('a')
    download = [
        (link.attrs['href'].split("/")[-1], link.get_text())
        for link in download
    ]

    return(
        render_template(
            'movie.html',
            movie_title=movie_title.get_text(),
            movie_year=movie_year.get_text(),
            movie_genre=movie_genre.get_text(),
            movie_thumbnail=movie_thumbnail.attrs['src'],
            movie_synopsis=movie_synopsis.get_text(),
            bottom_info=bottom_info.getText(),
            download=download
        )
    )
