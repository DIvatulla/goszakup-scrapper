def  is_whitespace(chr: str) -> bool:
	return ((chr == ' ') or (chr == '\r') or (chr == '\t') or (chr == '\n'))

class xml_node:
	def __init__ (self, tag: str, content: str):
		self.tag = tag
		self.content = content
		self.children = []

class xml_stack:
	def __init__ (self):
		self.data = []
		self.data.append(xml_node("root", ""))

	def __remove(self, tag: str):
		if tag == self.data[-1].tag:
			self.data.pop()
		else:
			raise Exception('Improperly closed/opened tag {}'.format(str(self.data[-1].tag)))

	def add(self, tag: str):
		if tag[0] == '/':
			self.__remove(tag)
		else:
			new_node = xml_node(tag, '')
			self.data[-1].children.append(new_node)
			self.data.append(new_node)

class xml_parser:
	def __init__(self, buf: str):
		self.doc = buf
		self.pos = 0
		self.lex_buf = ""
		self.xml_node_buf = []
		self.xml_node_stack = xml_stack()

	def __skip_whitespace(self):
		while is_whitespace(self.doc[self.pos]):
			self.pos += 1

			if self.pos > len(self.doc):
				raise Exception("Empty xml")
	
	def __skip_comment(self):
		while self.doc[self.pos] != '>':
			self.pos += 1

			if self.pos > len(self.doc):
				break
	
	def __read_tag(self):
		self.lex_buf = ""
		self.pos += 1
		
		while self.doc[self.pos] != '>':
			if self.doc[self.pos] == ' ':
				break
			else:
				self.lex_buf += self.doc[self.pos]
				self.pos += 1	
				
				if self.pos > len(self.doc):
					raise Exception(str('Unclosed tag in the document {}'.format(str(self.xml_node_stack.data[-1].tag))))

	def __read_content(self):
		self.lex_buf = ''
		
		if self.pos == 0:
			raise Exception("Content outside of root tag")
			
		while self.doc[self.pos] != '<':
			if not(is_whitespace(self.doc[self.pos])):
				self.lex_buf = self.lex_buf + self.doc[self.pos]
				
			self.pos += 1
			
			if self.pos >= len(self.doc):
				break

	def parse(self) -> xml_node:
		while self.pos < len(self.doc):
			self.__skip_whitespace() 
			
			if self.doc[self.pos] == '<' and self.doc[self.pos+1] != '!':
				self.xml_node_buf.append(self.xml_node_stack.data[-1])
				self.__read_tag()
				self.xml_node_stack.add(self.lex_buf)
			elif self.doc[self.pos] == '<' and self.doc[self.pos+1] == '!':
				self.__skip_comment()
			else:
				self.__read_content()
				self.pos -= 1
				self.xml_node_stack.data[-1].content = self.lex_buf
				
			self.pos += 1

		return self.xml_node_stack.data