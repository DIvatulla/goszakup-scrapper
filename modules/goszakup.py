from urllib.parse import quote
from urllib.parse import unquote
from http_module import https
from http_module import http_request
from http_module import http_response

class goszakup_filters:
	def __init__(self, name: str="", customer: str="", spec: str="",\
				number: str="", month: str="", year: str="", status: str="",\
				subject_type: str="", qvazi=""):
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
				res += quote("filter[{}][]={}&".format(item, filters_table[item][-1]), safe='/:=&')
			else:	
				res += quote("filter[{}]={}&".format(item, filters_table[item]), safe='/:=&')	

		res += "&count_record=50&page=1"
		return res

class goszakup:
	def __init__(self, filters: goszakup_filters):
		req = http_request(host="goszakup.gov.kz", path=filters.urlify(), headers={"Host": "goszakup.gov.kz", "User-Agent": "curl/8.14.1", "Content-Type": "*/*"})	
		self.data = https.get(req)	
	







