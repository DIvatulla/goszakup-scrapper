from urllib.parse import quote
from urllib.parse import unquote
from http_module import https
from http_module import http_request
from bs4 import BeautifulSoup
from openpyxl import Workbook
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
		self.__count_pages()

	def get_request(self) -> str:
		req = http_request(host="https://goszakup.gov.kz", path=(self.filters.urlify()), headers={"Host": "goszakup.gov.kz",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
		"Content-Type": "*/*"})	
		return https.get(req).text

	def __count_pages(self) -> int:
		self.count = 0
		st = 0
		html = self.get_request()
		
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

class excel:
	@classmethod
	def __parse_html(cls, html_doc: str) -> list:
		table = []
		soup = BeautifulSoup(html_doc, features="lxml")
		
		for tr in (soup.find_all('tbody')[1]).find_all('tr'):
			cells = tr.find_all('td')
			row = []
			
			for c in cells:
				buf = {}
				buf["content"] = c.get_text(strip=True)
				buf["url"] = None

				link_tag = c.find('a')
				if link_tag:
					url = link_tag.get('href')
					buf["url"] = url

				row.append(buf)
			
			table.append(row)

		return table

	@classmethod
	def make_table(cls, gz: goszakup, filename: str):
		wb = Workbook()
		ws = wb.active
		
		headers = ["#п/п", "Заказчик", "Наименование", "Способ_закупки",
				"Единица_измерения", "Кол-во", "Цена_за_ед", "Плановая_сумма",
				"Планируемый_срок_закупки", "Статус"]
		ws.append(headers)

		gz.filters.page = 0
		for i in range(gz.filters.count_record, gz.count, gz.filters.count_record):
			gz.filters.page += 1
			for row in cls.__parse_html(gz.get_request()):
				ws.append([cell_dict["content"] for cell_dict in row])
				
				for col_idx, cell_dict in enumerate(row, start=1):
					if cell_dict["url"]:
						cell_obj = ws.cell(row=ws.max_row, column=col_idx)
						cell_obj.hyperlink = cell_dict["url"]
						cell_obj.style = "Hyperlink"

			time.sleep(5)
		
		wb.save(filename)

				