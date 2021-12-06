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
		Lexer lex = new Lexer(inputFile);//����һ��Lexer�����ɨ����Taken�������ݸ�parser
		Parser parser = new Parser(lex);
		parser.program();//����parser����
		System.out.print("\n");
	}

}
