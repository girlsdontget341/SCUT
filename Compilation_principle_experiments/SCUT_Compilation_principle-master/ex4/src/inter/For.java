package inter;

import symbols.Type;

public class For extends Stmt {
	Expr expr;
	Stmt stmt1;
	Stmt stmt2;
	Stmt stmt3;

	public For() {
		expr = null;
		stmt1 = null;
		stmt2 = null;
		stmt3 = null;
	}

	public void init(Stmt s1, Expr x, Stmt s2, Stmt s3) {
		expr = x;
		stmt1 = s1;
		stmt2 = s2;
		stmt3 = s3;
		if (expr.type != Type.Bool)
			expr.error("boolean required in do");
	}

	public void gen(int b, int a) {
		//for(stmt1;expr;stmt2)
		//{	stmt3; }
		after = a; // save label a
		int labelExpr = newlabel();   //expr的标号
		int labelStmt3 = newlabel();   // label for stmt3
		int labelStmt2 = newlabel();     //stmt2的标号
		
		stmt1.gen(0, labelExpr); //生成stmt1
		
		emitlabel(labelExpr);
		expr.jumping(0, a); //如果不满足条件，跳出循环 
		emitlabel(labelStmt3);
		stmt3.gen(labelStmt3, labelStmt2);       //处理stmt3内部的
		
		emitlabel(labelStmt2);
		stmt2.gen(labelStmt2,a);     //生成stmt2代码
		emit("goto L" + labelExpr);   //跳转回条件判断处
		
	}

}
