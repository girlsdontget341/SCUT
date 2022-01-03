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
		int labelExpr = newlabel();   //expr�ı��
		int labelStmt3 = newlabel();   // label for stmt3
		int labelStmt2 = newlabel();     //stmt2�ı��
		
		stmt1.gen(0, labelExpr); //����stmt1
		
		emitlabel(labelExpr);
		expr.jumping(0, a); //�������������������ѭ�� 
		emitlabel(labelStmt3);
		stmt3.gen(labelStmt3, labelStmt2);       //����stmt3�ڲ���
		
		emitlabel(labelStmt2);
		stmt2.gen(labelStmt2,a);     //����stmt2����
		emit("goto L" + labelExpr);   //��ת�������жϴ�
		
	}

}
