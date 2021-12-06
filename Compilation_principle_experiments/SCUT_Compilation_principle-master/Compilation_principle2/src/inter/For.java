package inter;

import symbols.Type;

public class For extends Stmt{
	Expr expr; Stmt stmt;
	public For(){
		expr=null;
		stmt=null;
	}
	public void init(Stmt s, Expr x){
		expr = x; stmt = s;
		if( expr.type != Type.Bool ) expr.error("boolean required in for");
	}
	public void gen(int b, int a){}
	public void display(){
		emit("stmt : for begin");
		stmt.display();
		emit("stmt : for end");
	}
}
