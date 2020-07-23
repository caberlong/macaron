import sys
from antlr4 import *
from DataGeneratorLexer import DataGeneratorLexer
from DataGeneratorParser import DataGeneratorParser
from DataGeneratorParserListener import DataGeneratorParserListener


class PrintListener(DataGeneratorParserListener):
  def __init__(self):
    self._sub_protos = []
    self._var_values = {}

  def setProtoFieldValue(self, total_proto_path, value):
    print('set value %s to %s' % (value, total_proto_path))

  def getTotalProtoPath(self, ctx:DataGeneratorParser.ProtoPathContext, path:str=None):
    if ctx == None:
      return path
    if path == None:
      total_path = ctx.NAME().getText()
    else:
      total_path = ".".join([path, ctx.NAME().getText()])
    return self.getTotalProtoPath(ctx.protoPath(), total_path)

  def evalExpr(self, expr):
    if expr.NUMBER():
      return float(expr.NUMBER().getText())
    if expr.STRING():
      return expr.STRING().getText()
    if expr.refVar():
      return self.evalRefVar(expr.refVar())
    if expr.PLUS():
      return self.evalExpr(expr.left) + self.evalExpr(expr.right)
    if expr.MINUS():
      return self.evalExpr(expr.left) - self.evalExpr(expr.right)
    if expr.MULTI():
      return self.evalExpr(expr.left) * self.evalExpr(expr.right)
    if expr.DIV():
      return self.evalExpr(expr.left) / self.evalExpr(expr.right)
    if expr.expr():
      return self.evalExpr(expr.expr()[0])
    raise

  def evalRefVar(self, refVar):
    result = self._var_values[refVar.protoPath().NAME().getText()]
    proto_path = self.getTotalProtoPath(refVar.protoPath().protoPath())
    if proto_path != None:
      result = ".".join([result, proto_path])
    return result

  # Exit a parse tree produced by DataGeneratorParser#assignVariable.                             
  def exitAssignVariable(self, ctx:DataGeneratorParser.AssignVariableContext):                    
    self._var_values[ctx.NAME().getText()] = self.evalExpr(ctx.expr())
                                                                                                  
  # Enter a parse tree produced by DataGeneratorParser#assignSubProto.                            
  def enterAssignSubProto(self, ctx:DataGeneratorParser.AssignSubProtoContext):                   
    self._sub_protos.append(ctx.NAME().getText());
                                                                                                  
  # Exit a parse tree produced by DataGeneratorParser#assignSubProto.                             
  def exitAssignSubProto(self, ctx:DataGeneratorParser.AssignSubProtoContext):                    
    self._sub_protos.pop();

  # Exit a parse tree produced by DataGeneratorParser#assignField.                                
  def enterAssignField(self, ctx:DataGeneratorParser.AssignFieldContext):                          
    self.setProtoFieldValue(self.getTotalProtoPath(ctx.protoPath()), self.evalExpr(ctx.expr()))
    pass                                                                                        

                                                                                                  
def main(argv):
  input = FileStream(argv[1], encoding='utf-8')
  lexer = DataGeneratorLexer(input)
  stream = CommonTokenStream(lexer)
  parser = DataGeneratorParser(stream)
  tree = parser.generateDataProto()
  # print('tree: %s' % tree.getText())
  walker = ParseTreeWalker();
  listener = PrintListener();
  walker.walk(listener, tree);


if __name__ == '__main__':
  main(sys.argv)
