import json

from utils.v1.dummy import new_account, wrong_account_keys, wrong_account_firstname,\
    wrong_account_lastname, wrong_account_surname, wrong_account_portfolio,\
    wrong_account_occupation, wrong_account_phone, wrong_account_email,\
    wrong_account_password, wrong_account_cost, phone_exists, username_exists,\
    email_exists
from .base_test import BaseTest


class TestUsersAccount(BaseTest):
    """Testing the users account endpoint."""

    def test_create_account(self):
        """Test when a new user creates a new account."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Account created successfully!')
        assert response.status_code == 201

    def test_create_account_keys(self):
        """Test create account json keys."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_keys), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid username key')
        assert response.status_code == 400

    def test_account_firstname_input(self):
        """Test create account first name input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_firstname), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'First name is in wrong format')
        assert response.status_code == 400

    def test_account_lastname_input(self):
        """Test create account last name input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_lastname), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Last name is in wrong format')
        assert response.status_code == 400

    def test_account_surname_input(self):
        """Test create account surname input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_surname), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Surname is in wrong format')
        assert response.status_code == 400

    def test_account_portfolio_input(self):
        """Test create account portfolio input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_portfolio), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Portfolio should be either Education, Technical, Health or Domestic')
        assert response.status_code == 400

    def test_account_occupation_input(self):
        """Test create account occupation input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_occupation), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Occupation is in wrong format')
        assert response.status_code == 400

    def test_account_phone_input(self):
        """Test create account phone input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_phone), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid phone number!')
        assert response.status_code == 400

    def test_account_email_input(self):
        """Test create account email input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_email), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid email!')
        assert response.status_code == 400

    def test_account_password_input(self):
        """Test create account password input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_password), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character!')
        assert response.status_code == 400

    def test_account_cost_input(self):
        """Test create account cost input."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(wrong_account_cost), content_type='application/json')
        result = json.loads(response.data.decode())
        self.assertEqual(result['message'], 'Invalid cost value!')
        assert response.status_code == 400

    def test_create_account_with_an_existing_phone_number(self):
        """Test when a new user creates a new account with an existing phone number."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json')
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(phone_exists), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Phone number already exists!')
        assert response1.status_code == 400

    def test_create_account_with_an_existing_username(self):
        """Test when a new user creates a new account with an existing username."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json')
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(username_exists), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Username already exists!')
        assert response1.status_code == 400

    def test_create_account_with_an_existing_email(self):
        """Test when a new user creates a new account with an existing email."""

        response = self.client.post(
            '/api/v1/auth/register', data=json.dumps(new_account), content_type='application/json')
        response1 = self.client.post(
            '/api/v1/auth/register', data=json.dumps(email_exists), content_type='application/json')
        result = json.loads(response1.data.decode())
        self.assertEqual(result['message'], 'Email already exists!')
        assert response1.status_code == 400
