from src.database.models import Film


class FilmService:
    @staticmethod
    def fetch_all_films(session):
        return session.query(Film)

    @classmethod
    def fetch_all_films_by_uuid(cls, session, uuid):
        return cls.fetch_all_films(session).filter_by(uuid=uuid).first()