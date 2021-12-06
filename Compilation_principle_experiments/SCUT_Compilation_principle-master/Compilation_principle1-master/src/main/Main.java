package main;

import java.io.IOException;
import java.util.Hashtable;

import lexer.Lexer;
import lexer.Token;

public class Main {
	public static void main(String[] args) throws IOException {
		//载入词法分析器
		Lexer lexer = new Lexer();
		char c;
		do {
			Token token=lexer.scan();
			switch (token.tag) {
			case 270:
			case 272:
				System.out.println("(NUM , "+token.toString()+")");
				break;
			case 264:
				System.out.println("(ID , "+token.toString()+")");
				break;
			case 256:
			case 257:
			case 258:
			case 259:
			case 260:
			case 265:
			case 274:
			case 275:
			case 276:
			case 277:
			case 278:
			case 279:
			case 280:
			case 281:
			case 282:
				System.out.println("(KEY , "+token.toString()+")");
				break;
			case 283:
				//字符串
				System.out.println("(STR , "+token.toString()+")");
				break;
			case 520:
				break;
			//错误信息
			case 284:
				System.out.println("(ERR , "+token.toString()+")");
				break;
			default:
				System.out.println("(SYM , "+token.toString()+")");
				break;
			}

		} while (lexer.getPeek()!='\n');
	}
}
