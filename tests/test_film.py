import http
import json
from dataclasses import dataclass
from unittest.mock import patch

from src import app


@dataclass
class FakeFilm:
    title = "fake"
    distributed_by = "fake"
    release_date = "2010-10-21"
    description = "fake"
    length = 100
    rating = 0.0

class TestFilms:
    uuid =[]

    def test_get_films_with_db(self):
        client = app.test_client()
        resp = client.get('/films')

        assert resp.status_code == http.HTTPStatus.OK

    @patch('src.services.film_service.FilmService.fetch_all_films', autospec=True)
    def test_get_films_moke_db(self, mock_db_call):
        client = app.test_client()
        resp = client.get('/films')
        mock_db_call.assert_called_once()
        assert resp.status_code == http.HTTPStatus.OK

    def test_create_film_with_db(self):
        client = app.test_client()
        data = {
                "title": "test1dsf",
                "distributed_by": "test",
                "release_date": "2010-10-21",
                "description": "asd",
                "length": 100,
                "rating": 0.0
            }
        resp = client.post('/films', data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.CREATED
        assert resp.json["title"] == "test1dsf"
        self.uuid.append(resp.json["uuid"])

    def test_create_film_with_mock_db(self):
        with patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            client = app.test_client()
            data = {
                "title": "test1dsf",
                "distributed_by": "test",
                "release_date": "2010-11-21",
                "description": "asd",
                "length": 100,
                "rating": 0.0
            }
            resp = client.post('/films', data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_update_films_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        data = {
            "title": "test1dsu",
            "distributed_by": "tsadaest",
            "release_date": "2010-11-21",
            "description": "asd",
            "length": 100,
            "rating": 0.0
        }
        resp = client.put(url, data=json.dumps(data), content_type='application/json')
        assert resp.status_code == http.HTTPStatus.OK
        assert resp.json["title"] == 'test1dsu'

    def test_update_films_with_moke_db(self):

        with patch('src.services.film_service.FilmService.fetch_all_films_by_uuid') as mocked_query, \
                patch('src.db.session.add', autospec=True) as mock_session_add, \
                patch('src.db.session.commit', autospec=True) as mock_session_commit:
            mocked_query.return_value = FakeFilm
            client = app.test_client()
            url = f'/films/1'
            data = {
                "title": "test1dsu",
                "distributed_by": "tsadaest",
                "release_date": "2010-11-21",
                "description": "asd",
                "length": 100,
                "rating": 0.0
            }
            resp = client.put(url, data=json.dumps(data), content_type='application/json')
            mock_session_add.assert_called_once()
            mock_session_commit.assert_called_once()

    def test_delete_film_with_db(self):
        client = app.test_client()
        url = f'/films/{self.uuid[0]}'
        resp = client.delete(url)
        assert resp.status_code == http.HTTPStatus.NO_CONTENT