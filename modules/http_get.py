import http.client

class RequestErr(Exception):
	def __init__(self, res: http_response):
		self.err = {
			"status": res.status, 
			"response": res.body
		}

	def __str__(self):
		return json.dumps(self.err)

class http_request:
	def __init__(self, headers: dict = {}):
		self.path = "/"
		self.headers = headers

class http_response():
	def __init__(self, response: http.client.HTTPResponse | None = None):
		if response.status != 200:
			raise RequestErr(response)

		self.__parse_headers(response.headers)	
		self.body = response.read().decode()
		self.status = response.status

	def __parse_headers(self, headers):
		buf = []
		headers_dict = {}

		for line in re.split(r"\n", headers.as_string()):
			if len(line) < 1:
				continue

			buf = re.split(r": ", line, 1)
			headers_dict[buf[0]] = buf[1]

		return headers_dict

class http_getter:
	
