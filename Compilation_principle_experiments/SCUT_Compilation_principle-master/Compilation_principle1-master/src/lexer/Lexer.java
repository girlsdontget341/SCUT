package lexer;

import java.io.IOException;
import java.util.Hashtable;

public class Lexer {

	public static int line = 1;//默认行数为1
	char peek = ' ';
	Hashtable words = new Hashtable();//创建哈希表

	void reserve(Word w) {
		words.put(w.lexeme, w);
	}

	//设立关键字识别
	public Lexer() {
		reserve(new Word("if", Tag.IF));
		reserve(new Word("else", Tag.ELSE));
		reserve(new Word("while", Tag.WHILE));
		reserve(new Word("do", Tag.DO));
		reserve(new Word("break", Tag.BREAK));
		//在ppt基础上新增 void class static int for new return 等关键字
		reserve(new Word("void", Tag.VOID));
		reserve(new Word("class", Tag.CLASS));
		reserve(new Word("for", Tag.FOR));
		reserve(new Word("static", Tag.STATIC));
		reserve(new Word("int",Tag.INT));
		reserve(new Word("new",Tag.NEW));
		reserve(new Word("return",Tag.RETURN));
		reserve(new Word("basic",Tag.BASIC));
		reserve(new Word("index",Tag.INDEX));
		reserve(Word.True);
		reserve(Word.False);
	}

	//readch函数依次向后读取字符
	public void readch() throws IOException {
		peek = (char) System.in.read();
		
	}

	//readch 读一个字符 判断与参数c是否相等
	boolean readch(char c) throws IOException {
		readch();
		if (peek != c) {
			return false;
		}
		peek = ' ';
		return true;
	}

	public Token scan() throws IOException {
		//跳过空白符  对换行符实行跳行处理
		for (;; readch()) {
			if (peek == ' ' || peek == '\t')
				continue;
			else if (peek == '\n') {
				line += 1;
			} else {
				break;
			}
		}

		//判断是否为编程语言中有意义的符号
		switch (peek) {
		case '&':
			if (readch('&'))
				return Word.and;
			else
				return new Token('&');
		case '|':
			if (readch('|'))
				return Word.or;
			else
				return new Token('|');
		case '=':
			if (readch('='))
				return Word.eq;
			else
				return new Token('=');
		case '!':
			if (readch('='))
				return Word.ne;
			else
				return new Token('!');
		case '<':
			if (readch('='))
				return Word.le;
			else
				return new Token('<');
		case '>':
			if (readch('='))
				return Word.ge;
			else
				return new Token('>');
		}


		//处理输入的字符串
		if(peek=='\"')
		{
			StringBuffer s=new StringBuffer();
			do {
				readch();
				if(peek=='\"')
					break;
				s.append(peek);
			} while (peek!='\"');
			peek=' ';
			return new Word(s.toString(),Tag.STRING);
		}

		//处理注释
		if(peek=='/')
		{
			StringBuffer s=new StringBuffer();
			//处理单行注释
			if(readch('/'))
			{
				do {
					readch();
					if(peek=='\n')
						break;
					s.append(peek);
				} while (peek!='\n');
				peek=' ';
				return new Token(520);
			}

			//处理多行注释
			if(peek=='*')
			{
				int count=0;
				do {
					if(readch('*')) {
						if(readch('/'))
							break;
						else
							s.append('*');
					}
					s.append(peek);
				} while (true);
				peek=' ';
				return new Token(520);
			}
		}



		//检测数字
		if (Character.isDigit(peek)) {
			//用于获取整数 同时也是获取浮点数的非小数部分
			int zero_count=0;
			int v = 0;
			do {
				if(Character.digit(peek,10)==0)
					zero_count+=1;
				v = 10 * v + Character.digit(peek, 10);
				readch();
			} while (Character.isDigit(peek));




			//获取浮点数 小数部分
			if (peek == '.')
			{
				float x = v;
				float d = 10;
				StringBuffer sb=new StringBuffer();
				for (;;) {
					readch();
					//获取12.2E+2这种形式的浮点数
					if (!Character.isDigit(peek))
					{
						sb.append(x);
						if(peek=='E'||peek=='e')
						{
							sb.append(peek);
							readch();
							if(peek=='-'||peek=='+')
							{
								sb.append(peek);
								v=0;
								readch();
								do {
									v = 10 * v + Character.digit(peek, 10);
									readch();
								} while (Character.isDigit(peek));
								sb.append(v);
								return new Real(Float.parseFloat(sb.toString()));
							}
							else
								return new Word("Decimal indicates an error!"+" "+sb.toString(),Tag.ERR);
						}
						else
						break;
					}

					x = x + Character.digit(peek, 10) / d;
					d = d * 10;
				}
				return new Real(x);
			}

			//获取16进制整数
			if((peek=='x'&&v==0&&zero_count==1)||(peek=='X'&&v==0&&zero_count==1))
			{
				StringBuffer sb = new StringBuffer();
				sb.append("0"+peek);
				readch();
				do {
					if(Character.isDigit(peek)||(peek>='A'&&peek<='F'))
						sb.append(peek);
					else
						break;
					readch();
				} while (Character.isLetterOrDigit(peek));
				if(sb.length()>2)
				return new Num(Integer.parseInt(sb.toString().substring(2),16));
				else
					return new Word("Hexadecimal integer indicates an error!"+" "+sb.toString(),Tag.ERR);
			}

			return new Num(v);
		}
		//这边是判别是否为标识符的
		if (Character.isLetter(peek)) {
			StringBuffer b = new StringBuffer();
			do {
				b.append(peek);
				readch();
			} while (Character.isLetterOrDigit(peek)||peek=='_');//这里实现下划线加入标识符

			//缓存
			String s = b.toString();
			Word w = (Word) words.get(s);
			if (w != null)
				return w;
			w = new Word(s, Tag.ID);
			words.put(s, w);
			return w;
		}
		//检测输入中是否存在不合法字符 直接报错
		if(peek=='+'||peek=='-'||peek=='*'||peek=='/'||peek=='%'
		||peek==';'||peek==','||peek=='.'||peek=='{'||peek=='}'
		||peek=='('||peek==')'||peek=='['||peek==']')
		{
			Token tok = new Token(peek);
			peek = ' ';
			return tok;
		}
		else
		{
			Word word=new Word("Illegal character in identifier! "+String.valueOf(peek),284);
			peek=' ';
			return word;
		}
	}
	
	public void out() {
		System.out.println(words.size());
		
	}

	public char getPeek() {
		return peek;
	}

	public void setPeek(char peek) {
		this.peek = peek;
	}

}
