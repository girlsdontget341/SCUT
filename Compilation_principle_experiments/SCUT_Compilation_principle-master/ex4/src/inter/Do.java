package inter;

import symbols.Type;

public class Do extends Stmt {

   Expr expr; Stmt stmt;

   public Do() { expr = null; stmt = null; }

   public void init(Stmt s, Expr x) {
      expr = x; stmt = s;
      if( expr.type != Type.Bool ) expr.error("boolean required in do");
   }

   public void gen(int b, int a) {
      after = a;
      int label = newlabel();   // label for expr, 给 expr 一个标号
      stmt.gen(b,label);        // 产生表达式的三地址指令
      emitlabel(label);
      expr.jumping(b,0);
   }
}