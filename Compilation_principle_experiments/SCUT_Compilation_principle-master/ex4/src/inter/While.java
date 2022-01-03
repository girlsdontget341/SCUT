package inter;

import symbols.Type;

public class While extends Stmt {

	Expr expr;
	Stmt stmt;

	public While() {
		expr = null;
		stmt = null;
	}

	public void init(Expr x, Stmt s) {
		expr = x;
		stmt = s;
		if (expr.type != Type.Bool)
			expr.error("boolean required in while");
	}

	public void gen(int b, int a) {
		after = a; // save label a
		expr.jumping(0, a);     //条件不满足则跳转到结束
		int label = newlabel(); // label for stmt
		emitlabel(label);       //output 循环体的开始标号
		stmt.gen(label, b);     //处理stmt内部的
		emit("goto L" + b);     //每次循环后要跳转回开始
	}
}
