import http.client
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
	def __init__(self, host: str, path: str, headers: dict = {}, body: dict = {}):
		self.host = host
		self.path = "/"
		self.headers = headers
		self.body = body

class http_response:
	def __init__(self, response: http.client.HTTPResponse | None = None):
		if response.status != 200:
			raise RequestErr(response)

		self.headers = self.__parse_headers(response.headers)	
		self.body = response.read().decode()
		self.status = response.status

	def __parse_headers(self, headers) -> dict:
		buf = []
		headers_dict = {}

		for line in re.split(r"\n", headers.as_string()):
			if len(line) < 1:
				continue

			buf = re.split(r": ", line, 1)
			headers_dict[buf[0]] = buf[1]

		return headers_dict

class https():
	@staticmethod	
	def get(req: http_request, port: int=443):
		connection = http.client.HTTPSConnection(req.host, port, timeout=30)
		connection.request("GET", req.path, json.dumps(req.body), req.headers)
		response = http_response(connection.getresponse())
		connection.close()
		return response
