""" Mongo Connection is the base class that all the model classes
should extend """

from pymongo import Connection

class MongoConnection :

	""" Hopefully this is a static class variable """
	db = None

	"""Get a Mongo connection"""
	def __init__(self):
		if self.db is None :
			connection = Connection()
			self.db = connection.mynews

	"""Utility method to reverse a cursor"""
	def reverse(self, cursor) :
		reversed = []
		for row in cursor :
			reversed.insert(0,row)
		return reversed
