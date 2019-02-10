from flask import Blueprint, Response
import requests
import json
from bs4 import BeautifulSoup

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/page/<page>', methods=('POST', 'GET'))
def api(page):
    req = requests.get("https://yts.am/browse-movies?page={0:s}".format(page))
    if req.status_code != 200:
        return(
            Response(
                "\{'status': 'http error', 'code': {0:d}\}".format(
                    req.status_code
                ),
                200,
                {'content-type': 'application/json'}
            )
        )

    soup = BeautifulSoup(req.text, "html.parser")
    movies_html = soup.find_all('div', class_="browse-movie-wrap")
    movies = {}
    n = 0
    for movie_html in movies_html:
        #print(movie_html)
        movie_title = movie_html.find_all('a', class_="browse-movie-title")[0]
        movie_thumbnail = movie_html.find_all(
            'img', class_="img-responsive"
        )[0]
        movies[n] = {
            'title': movie_title.get_text(),
            'href': movie_title.attrs['href'],
            'thumbnail': movie_thumbnail.attrs['src']
        }
        n += 1

    return(
        Response(
            json.dumps(movies),
            200,
            {'content-type': 'text/html'}
        )
    )
