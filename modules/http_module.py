import requests
import json
import re
from abc import ABC

class RequestErr(Exception):
	def __init__(self, res):
		self.err = {
			"status": res.status, 
			"response": res.body
		}

	def __str__(self):
		return json.dumps(self.err)

class http_request:
	def __init__(self, host: str, path: str="/", headers: dict = {}, body: dict = {}):
		self.host = host
		self.path = path
		self.headers = headers
		self.body = body

class https():
	@staticmethod	
	def get(req: http_request, port: int=443):
		session = requests.Session()
		session.get(req.host)
		response = requests.get('{}{}'.format(req.host, req.path), req.headers)
		return response
