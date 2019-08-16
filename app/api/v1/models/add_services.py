import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database
from datetime import datetime
import psycopg2


class AddServicesModel(Database):
    """A registered user can add a service."""

    def __init__(self, service_provider=None, portfolio=None, occupation=None, location=None, cost=None):
        super().__init__()
        self.service_provider = service_provider
        self.portfolio = portfolio
        self.occupation = occupation
        self.location = location
        self.cost = cost

    def save(self):
        """Save information of the service."""

        try:
            self.curr.execute(
                ''' INSERT INTO add_services(service_provider, portfolio, occupation, location, cost)\
                    VALUES('{}','{}','{}','{}','{}') RETURNING service_provider, portfolio, occupation, location, cost''' \
                    .format(self.service_provider, self.portfolio, self.occupation, self.location, self.cost))
            service = self.curr.fetchone()
            self.conn.commit()
            self.curr.close()
            return service
            

            query = """
					SELECT users.username FROM add_services\
					INNER JOIN users ON add_services.service_provider=users.user_id;
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

        query = "SELECT * from add_services"
        services = Database().fetch(query)
        return json.dumps(services, default=str)

    def get_service(self, occupation):
        """Get a service with specific occupation."""

        self.curr.execute(''' SELECT * FROM add_services WHERE occupation=%s''', (occupation,))
        service = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(service, default=str)
