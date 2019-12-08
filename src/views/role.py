"""Roles Resource Module"""

# third party library
from flask_restplus import Resource
from flask import request

from app import api


@api.route('/role')
class RoleResource(Resource):
	"""Roles Resource"""
	
	def get(self):
		"""
		Get roles
		"""
		
		return {
			"data": {
				
				'name': 'admin',
			}
		}
