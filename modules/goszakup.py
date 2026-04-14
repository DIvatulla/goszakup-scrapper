from urllib.parse import quote
from urllib.parse import unquote
from http_module import https
from http_module import http_request
from bs4 import BeautifulSoup
import time
import re

class goszakup_filters:
	def __init__(self, name: str="", customer: str="", spec: str="",\
				number: str="", month: str="", year: str="", status: str="",\
				subject_type: str="", qvazi: str="",\
				count_record: int=50, page: int=1):
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
		res = "/ru/registry/plan?"
		filters_table = dict(self)

		for item in filters_table:
			if type(filters_table[item]) == list:
				if filters_table[item][-1] == '':
					continue
				
				res += quote("filter[{}][]={}&".format(item, filters_table[item][-1]), safe='/:=&')
			else:
				if filters_table[item] == '':
					continue

				res += quote("filter[{}]={}&".format(item, filters_table[item]), safe='/:=&')	

		res += "count_record={}&page={}".format(self.count_record, self.page)
		return res

class goszakup:
	def __init__(self, filters: goszakup_filters):
		self.filters = filters

	def __get_request(self) -> str:
		req = http_request(host="https://goszakup.gov.kz", path=(self.filters.urlify()), headers={"Host": "goszakup.gov.kz",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
		"Content-Type": "*/*"})	
		return https.get(req).text

	def __count_pages(self) -> int:
		self.count = 0
		st = 0
		html = self.__get_request()
		
		for line in html.splitlines():
			match st:
				case 0:
					if "<small class=\"text-muted\">" in line:
				  		st += 1
				  		continue
				case 1:
					match = re.search(f"{r"из "}(.*?){r" записей"}", line)
					self.count = int(match.group(1))
					break
	
	def __get_all_pages(self):
		self.buf = []
		self.__count_pages()

		for i in range(50, self.count, 50):
			self.filters.number = i
			self.buf.append(self.__get_request())
			time.sleep(5)
			print(self.buf[-1])

	def __parse_html(self):
		rows = []
		self.__get_all_pages()

		for page in self.buf:
			soup = BeautifulSoup(page, features="lxml")
			for tr in (soup.find_all('tbody')[1]).find_all('tr'):
				cells = tr.find_all('td')
				row_data = [c.get_text(strip=True) for c in cells]
				rows.append(row_data)
		
		self.rows = rows

	def make_table(self):
		self.__get_all_pages()
		self.__parse_html()

		print("#п/п;Заказчик;Наименование;Способ;закупки;Единица_измерения;Кол-во;Цена_за_ед.;Плановая_сумма;Планируемый_срок_закупки;Статус")
		for r in self.rows:
			print(";".join(r))