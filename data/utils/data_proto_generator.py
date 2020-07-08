import sys
from antlr4 import *
from DataGeneratorLexer import DataGeneratorLexer
from DataGeneratorParser import DataGeneratorParser
from DataGeneratorParserListener import DataGeneratorParserListener
from data.proto import data_pb2


class DataProtoGenerator:
  def __init__(self):
    pass

  class Listener(DataGeneratorParserListener):
    def __init__(self, data_proto):
      self._sub_protos = []
      self._proto_paths = []
      self._var_values = {}
      self._data_proto = data_proto

    def setProtoFieldValue(self, total_proto_path, value):
      print('set value %s to %s' % (value, total_proto_path))

    def getTotalProtoPath(self):
      return '.'.join(self._sub_protos + self._proto_paths)

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
      return self._var_values[refVar.NAME().getText()]

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
    def exitAssignField(self, ctx:DataGeneratorParser.AssignFieldContext):                          
      self.setProtoFieldValue(self.getTotalProtoPath(), self.evalExpr(ctx.expr()))
      self._proto_paths.clear()
      pass                                                                                        
                                                                                                    
    # Enter a parse tree produced by DataGeneratorParser#protoPath.                                 
    def enterProtoPath(self, ctx:DataGeneratorParser.ProtoPathContext):                             
      self._proto_paths.append(ctx.NAME().getText())

  def generateDataProto(self, config: str):
    data_proto = data_pb2.Data()
    lexer = DataGeneratorLexer(InputStream(config))
    stream = CommonTokenStream(lexer)
    parser = DataGeneratorParser(stream)
    tree = parser.generateDataProto()
    walker = ParseTreeWalker();
    listener = self.Listener(data_proto);
    walker.walk(listener, tree);
    return data_proto;
