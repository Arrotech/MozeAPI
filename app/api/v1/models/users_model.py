import json
from werkzeug.security import generate_password_hash
from app.api.v1.models.database import Database


class UsersModel(Database):
    """Add a new user and retrieve User(s) by Id, Admission Number or Email."""

    def __init__(self, firstname=None, lastname=None, surname=None, phone=None, location=None, portfolio=None, occupation=None, username=None, email=None, password=None, cost=None):
        super().__init__()
        self.firstname = firstname
        self.lastname = lastname
        self.surname = surname
        self.phone = phone
        self.location = location
        self.portfolio = portfolio
        self.occupation = occupation
        self.username = username
        self.email = email
        if password:
            self.password = generate_password_hash(password)
        self.cost = cost

    def save(self):
        """Save information of the new user."""
        self.curr.execute(
            ''' INSERT INTO users(firstname, lastname, surname, phone, location, portfolio, occupation, username, email, password, cost)\
                VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}',{}) RETURNING firstname, lastname, surname, phone, location, portfolio, occupation, username, email, password, cost''' \
                .format(self.firstname, self.lastname, self.surname, self.phone, self.location, self.portfolio, self.occupation, self.username, self.email, self.password,
                        self.cost))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_username(self, username):
        """Request a single user with specific Username."""
        self.curr.execute(""" SELECT * FROM users WHERE username=%s""", (username,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_email(self, email):
        """Request a single user with specific Email Address."""
        self.curr.execute(''' SELECT * FROM users WHERE email=%s''', (email,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)

    def get_phone(self, phone):
        """Request a single user with specific Email Address."""
        self.curr.execute(''' SELECT * FROM users WHERE phone=%s''', (phone,))
        user = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return json.dumps(user, default=str)