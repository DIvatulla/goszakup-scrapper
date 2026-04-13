def  is_whitespace(chr: str){
	return ((chr == ' ') || (chr == '\r') || (chr == '\t') || (chr == '\n'));
}

class xml_node:
    def __init__(self, tag: str, content: str):
		self.tag = tag
		self.content = content
		self.children = []
}

class xml_stack:
    def __init__(self):
        self.data = []
        self.data.append(xml_node("root", ""))

	def __remove(tag: str){
		if tag == this.head.data.tag:
			self.data.pop()
		else:
			raise Exception('Improperly closed/opened tag {}'.format(
                str(self.data[-1])))
	}

	def add(tag: str):
		if tag[0] == '/':
			self.__remove(tag);
		else:
            new_node = xml_node(tag, '')
			this.data[-1].children.append(new_node)
			this.data.append(new_node)

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

			if self.pos > self.doc.length:
				raise Exception('Empty xml')				
	
    def __read_tag(self):
        self.lex_buf = ""
        self.pos += 1

		while self.doc[self.pos] != '>':
            if self.doc[self.pos] == ' ':
                break
            else:
                self.lex_buf = self.lex_buf + self.doc[self.pos]
			    self.pos += 1	
			
			    if self.pos > len(self.doc):
                    raise Exception(str('Unclosed tag in the document {}'.format(self.xml_node_stack.data[-1].tag)))


	def __read_content(self):
		self.lex_buf = ''
		
		if self.pos == 0:
			raise Exception("Content outside of root tag")

		while self.doc[self.pos] != '<':
			if !is_whitespace(self.doc[self.pos]):
				self.lex_buf = self.lex_buf + this.doc[this.pos]
			
            self.pos += 1	
			
			if self.pos >= self.doc.length: 
				break

	def parse(self):
		while self.pos < len(self.doc){
			this.#skip_whitespace();    
	
			if (this.doc[this.pos] === '<'){
				this.xmlNodeBuf.push(this.xmlNodeStack.head.data);
				this.#read_tag();
				this.xmlNodeStack.add(this.lexBuf);
			}				
			else{
				this.#read_content();
				this.pos--;
				this.xmlNodeStack.head.data.content = this.lexBuf;	
			}
			this.pos++;
		}

		if (this.xmlNodeStack.head.next !== null){
			throw new Error('Unclosed tag in the document ' + 
					JSON.stringify({'tag':this.xmlNodeStack.head.data.tag}));
		}
		if (this.xmlNodeStack.head.data.children.length > 1){
			throw new Error('More than one root tag in the document');
		}
		
		this.xmlNodeStack.pop();	
		return this.xmlNodeBuf[this.xmlNodeBuf.length-1];
	}
}
