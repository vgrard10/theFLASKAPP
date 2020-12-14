import unittest
from flask import current_app
from app import app, db
import os

class TestOnApp(unittest.TestCase):
	"""Check some app configuration"""
	def setUp(self):
		self.app = app
		self.app_context = self.app.app_context()
		self.app_context.push()

	def tearDown(self):
		self.app_context.pop()

	def test_app_exists(self):
		self.assertIsNotNone(current_app)

	def test_valid_secret_key(self):
		"""assert whether SECRET_KEY env variable is set to something different from the default unsafe value"""
		self.assertNotEqual(current_app.config["SECRET_KEY"], 
			"hard to guess string")