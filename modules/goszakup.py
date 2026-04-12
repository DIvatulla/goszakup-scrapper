from urllib.parse import quote
from urllib.parse import unquote

class filters:
	def __init__(self, name, customer, spec, number, month, year, status, subject_type, qvazi):
		self.name = name
		self.customer = customer
		self.number = number
		self.month = [month]
		self.year = [year]
		self.status = status
		self.subject_type = [G]
		self.qvazi = qvazi

	def __iter__(self):
		for attr, value in self.__dict__.iteritems():
			yield attr, value	 

	def urlify() -> str:
		res = "goszakup.gov.kz/ru/registry/plan?"
		filters_table = dict(self)

		for item in filters_table:
			if type(filters_table[item]) == list:
				res += "filter[{}][]?".format(filters_table[item])	
			else:
				res += "filter[{}]?".format(filters_table[item])	

		return res


