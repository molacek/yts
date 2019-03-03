from flask import Blueprint, Response, request
from werkzeug.contrib.cache import MemcachedCache
import requests
import json
from bs4 import BeautifulSoup

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/page/<page>', methods=('POST',))
def page(page):

    req_text = None
    cache = MemcachedCache(['127.0.0.1:11211'])
    search = request.form.get("search")
    if search:
        url = (
            "https://yts.am/browse-movies/"
            "{0:s}/all/all/0/latest".format(search)
        )
        if page > "1":
            url = "{0:s}?page={1:s}".format(url, page)
    else:
        url = (
            "https://yts.am/browse-movies?page={0:s}".format(page)
        )
        req_text = cache.get("page_{0:s}".format(page))

    if req_text is None:
        print(url)

        req = requests.get(url)
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
        req_text = req.text
        if not search:
            cache.set("page_{0:s}".format(page), req_text)

    soup = BeautifulSoup(req_text, "html.parser")
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
            'href': movie_title.attrs['href'].split('/')[-1],
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


@bp.route('/download/<id>', methods=('POST',))
def download(id):

    req = requests.get(
        "https://yts.am/torrent/download/{0:s}".format(id),
        stream=False
    )

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

    filename = "/home/lukas/transmission/{0:s}".format(
        req.headers["Content-disposition"].split('=')[-1].strip('"')
    )
    print(filename)

    with open(filename, 'wb') as f:
        for chunk in req.iter_content(chunk_size=1024):
            f.write(chunk)

    return(
        Response(
            "{'status': 'OK'}",
            200,
            {'content-type': 'application/json'}
        )
    )
