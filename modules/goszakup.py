from urllib.parse import quote
from urllib.parse import unquote
from http_module import https
from http_module import http_request
from http_module import http_response

class goszakup_filters:
	def __init__(self, name: str="", customer: str="", spec: str="",\
				number: str="", month: str="", year: str="", status: str="",\
				subject_type: str="G", qvazi=""):
		self.name = name
		self.customer = customer
		self.number = number
		self.month = [month]
		self.year = [year]
		self.status = status
		self.subject_type = subject_type
		self.qvazi = qvazi

	def __iter__(self):
		for attr, value in self.__dict__.items():
			yield attr, value	 

	def urlify(self) -> str:
		res = "goszakup.gov.kz/ru/registry/plan?"
		filters_table = dict(self)

		for item in filters_table:
			if type(filters_table[item]) == list:
				res += quote("filter[{}][]?".format(filters_table[item]))
			else:
				res += quote("filter[{}]?".format(filters_table[item]))	

		return res

class goszakup_parser:

class goszakup:
	def __init__(self, filters: goszakup_filters):
		req = http_request("goszakup.gov.kz", filters.urlify(), {"Content-Type": "*/*"})	
		self.data = https.get(req)	
	







