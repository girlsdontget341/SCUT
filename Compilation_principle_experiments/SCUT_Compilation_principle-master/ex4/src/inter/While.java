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
		expr.jumping(0, a);     //��������������ת������
		int label = newlabel(); // label for stmt
		emitlabel(label);       //output ѭ����Ŀ�ʼ���
		stmt.gen(label, b);     //����stmt�ڲ���
		emit("goto L" + b);     //ÿ��ѭ����Ҫ��ת�ؿ�ʼ
	}
}
