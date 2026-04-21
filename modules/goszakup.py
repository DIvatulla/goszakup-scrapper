from urllib.parse import quote
from urllib.parse import unquote
from http_module import https
from http_module import http_request
from bs4 import BeautifulSoup
from openpyxl import Workbook
from urllib.parse import urlsplit
import time
import re
import requests
from requests.adapters import HTTPAdapter

class goszakup_filters:
	def __init__(self, name: str="", customer: str="", spec: str="",\
				number: str="", month: str="", year: str="", status: str="",\
				subject_type: str="", qvazi: str="",\
				count_record: int=2000, page: int=1):
		self.name = name
		self.customer = customer
		self.number = number
		self.month = [month]
		self.year = [year]
		self.status = status
		self.subject_type = subject_type
		self.qvazi = qvazi
		self.count_record = count_record
		self.page = page

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
		self.host = "https://goszakup.gov.kz"
		self.adapter = HTTPAdapter(max_retries=3)
		self.session = requests.Session()
		self.session.mount('https://goszakup.gov.kz', self.adapter)
		self.session.headers.update({
			"Host": "goszakup.gov.kz",
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0",
			"Content-Type": "*/*"
		})
		self.__count_pages()

	def get_request(self) -> str:
		return self.session.get('{}{}'.format(self.host, self.filters.urlify())).text	

	def __count_pages(self) -> int:
		self.count = 0
		html_doc = self.get_request()
		soup = BeautifulSoup(html_doc, features="lxml")
		text = ((soup.find_all("small")[0]).find("strong")).get_text(strip=True)
		match = re.search(f"{r"из "}(.*?){r" записей"}", text)
		self.count = int(match.group(1))
		
class excel:
	@classmethod
	def parse_cell(cls, c) -> dict:
		result = {"content": None, "url": None}

		url_tag = c.find('a')
		if url_tag:
			result["url"] = url_tag.get('href')

		result["content"] = c.get_text(strip=True)

		return result

	@classmethod
	def parse_html(cls, html_doc: str) -> list:
		table = []
		soup = BeautifulSoup(html_doc, features="lxml")
		
		for tr in ((soup.find_all('tbody')[1]).find_all('tr')):
			cells = tr.find_all('td')
			(list(map(
				lambda x: table.append(x),
				(list(map(lambda cell: cls.parse_cell(cell), cells)))
			)))

		return table

	@classmethod
	def make_table(cls, gz: goszakup, filename: str):
		wb = Workbook()
		ws = wb.active

		for i in range(gz.filters.count_record, gz.count+gz.filters.count_record, gz.filters.count_record):
			gz.filters.page += 1
			for row in cls.parse_html(gz.get_request()):
				if (row["content"] == '') and (row["url"] != None):
					time.sleep(5)
					res = gz.session.get(row["url"]).text
					soup = BeautifulSoup(res, features="lxml")
					row["content"] = (soup.find_all('title')[0]).get_text(strip=True)

				ws.append([cell_dict["content"] for cell_dict in row])
				for col_idx, cell_dict in enumerate(row, start=1):
					if cell_dict["url"]:
						print(cell_dict)
						cell_obj = ws.cell(row=ws.max_row, column=col_idx)
						cell_obj.hyperlink = cell_dict["url"]
						cell_obj.style = "Hyperlink"
				
				time.sleep(10)

		wb.save(filename)