import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime
import psycopg2


class SeekServicesModel(Database):
    """A registered user can seek a service."""

    def __init__(self, service_seeker=None, service=None, cost=None):
        super().__init__()
        self.service_seeker = service_seeker
        self.service = service
        self.cost = cost

    def save(self):
        """Save information of the service."""

        try:
            self.curr.execute(
                ''' INSERT INTO seek_services(service_seeker, service, cost)\
                    VALUES('{}','{}','{}') RETURNING service_seeker, service, cost''' \
                    .format(self.service_seeker, self.service, self.cost))
            service = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return service


            query = """
					SELECT users.username, add_services.occupation FROM seek_services\
                    INNER JOIN users ON seek_services.service_seeker=users.user_id\
					INNER JOIN add_services ON seek_services.service=add_services.service_id;
					"""

            service = self.curr.fetchall()

            self.curr.execute(query)
            self.conn.commit()
            self.curr.close()

            return json.dumps(service, default=str)
        except psycopg2.IntegrityError:
            return "error"

    def get_services(self):
        """Fetch all services."""

        query = "SELECT * from seek_services"
        services = Database().fetch(query)
        return json.dumps(services, default=str)

    def get_service(self, service):
        """Get a service with specific service."""

        self.curr.execute(''' SELECT * FROM seek_services WHERE service=%s''', (service,))
        service = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(service, default=str)
