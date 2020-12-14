import unittest
from app import app, db, User
import os
from utils import ping, connect_to_db_server

class TestsOnEnvVars(unittest.TestCase):

	def test_postgres_env_vars_are_set(self):
		"""assert whether postgres-related env variables are defined"""
		self.assertIsNotNone(os.getenv("POSTGRES_PASSWORD"))
		self.assertIsNotNone(os.getenv("POSTGRES_USER"))
		self.assertIsNotNone(os.getenv("POSTGRES_DB"))
	
	def test_use_postgres_env_var_is_set(self):
		"""assert whether use of postgres related env variable is defined"""
		self.assertIsNotNone(os.getenv("USE_POSTGRES"))

class TestIsPostgresReachable(unittest.TestCase):
	"""Check the Postgres service is reachable"""

	def setUp(self):
		self.pguser = os.getenv("POSTGRES_USER")
		self.pgpass = os.getenv("POSTGRES_PASSWORD")
		self.pgdb   = os.getenv("POSTGRES_DB")

	def test_is_postgres_service_reachable(self):
		"""Check the Postgres service is reachable by pinging it"""
		self.assertTrue(ping("db"))

	def test_connect_to_postgres_db(self):
		"""Check if the app can connect to the postgres db hosted on the postgres server using the right credentials set on both ends"""
		self.connection = connect_to_db_server(
				self.pguser, self.pgpass, self.pgdb)
		self.assertIsNotNone(self.connection)

#class LoadUserInPostgresDbUseCase(unittest.TestCase):
#	""" Check the Postgres service is reachable """
#	def setUp(self):
#		self.app = app
#		self.app_context = self.app.app_context()
#		self.app.testing = True
#		self.app_context.push()
#		db.create_all()
#
#	def test_load_user(self):
#		""" Check the Postgres service is reachable by pinging it"""
#		#self.assertTrue(ping("db"))
#		print( self.app.config)
#		with self.app.test_client() as client:
#			print( self.app.config)
#			client.post("/predict", 
#				data=dict(name="Luc", age=25, 
#					ticket_price=100, sexe=True))
#			self.assertIsNotNone(User.query.first())
#			
#	def tearDown(self):
#		db.session.remove()
#		db.drop_all()
#		self.app_context.pop()

