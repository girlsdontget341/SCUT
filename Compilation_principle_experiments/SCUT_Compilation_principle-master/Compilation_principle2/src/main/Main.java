package main;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;

import parser.Parser;
import lexer.Lexer;

public class Main {

	public static void main(String[] args) throws IOException {
		File inFile = new File("in.txt");
		if(!inFile.exists()){
			System.out.println("InFile does not exist.");
			System.exit(1);
		}
		FileInputStream inputFile = new  FileInputStream(inFile);
		// TODO Auto-generated method stub
		Lexer lex = new Lexer(inputFile);//创建一个Lexer类对象，扫描获得Taken串并传递给parser
		Parser parser = new Parser(lex);
		parser.program();//进行parser处理
		System.out.print("\n");
	}

}
