package inter;

import symbols.Type;

public class If extends Stmt {

	Expr expr;
	Stmt stmt;

	public If(Expr x, Stmt s) {
		expr = x;
		stmt = s;
		if (expr.type != Type.Bool)
			expr.error("boolean required in if");
	}

	public void gen(int b, int a) {
		int label = newlabel(); // label for the code for stmt
								//产生一个新的内部使用的标号，用于条件判断后的跳转
		expr.jumping(0, a); // fall through on true, goto a on false
							// false 跳转到结束标号
		emitlabel(label);	//output中间标号
		stmt.gen(label, a); 
	}
}
