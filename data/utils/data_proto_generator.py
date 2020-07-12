import sys
from antlr4 import *
from DataGeneratorLexer import DataGeneratorLexer
from DataGeneratorParser import DataGeneratorParser
from DataGeneratorParserListener import DataGeneratorParserListener
from data.proto import data_pb2
from google.protobuf import message_factory


class DataProtoGenerator:
  def __init__(self):
    pass

  class Listener(DataGeneratorParserListener):
    def __init__(self, data_proto: data_pb2.Data):
      self._scopes = [data_proto]
      self._proto_paths = []
      self._var_values = {}

    def setFieldValue(self, value):
      scope_field = self._scopes[-1]
      for path in self._proto_paths[:-1]:
        scope_field = getattr(scope_field, path)
      setattr(scope_field, self._proto_paths[-1], value)

    def pushScope(self, field_name):
      """push the field message as the current scope."""
      self._scopes.append(getattr(self._scopes[-1], field_name))

    def popScope(self):
      self._scopes.pop()

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
      self.pushScope(ctx.NAME().getText())
                                                                                                    
    # Exit a parse tree produced by DataGeneratorParser#assignSubProto.                             
    def exitAssignSubProto(self, ctx:DataGeneratorParser.AssignSubProtoContext):                    
      self.popScope()

    # Exit a parse tree produced by DataGeneratorParser#assignField.                                
    def exitAssignField(self, ctx:DataGeneratorParser.AssignFieldContext):                          
      self.setFieldValue(self.evalExpr(ctx.expr()))
      self._proto_paths.clear()
      pass                                                                                        
                                                                                                    
    # Enter a parse tree produced by DataGeneratorParser#protoPath.                                 
    def enterProtoPath(self, ctx:DataGeneratorParser.ProtoPathContext):                             
      self._proto_paths.append(ctx.NAME().getText())

  def generateDataProto(self, config: str, data_proto: data_pb2.Data):
    lexer = DataGeneratorLexer(InputStream(config))
    stream = CommonTokenStream(lexer)
    parser = DataGeneratorParser(stream)
    tree = parser.generateDataProto()
    walker = ParseTreeWalker();
    listener = self.Listener(data_proto);
    walker.walk(listener, tree);
    print('Data proto output: %s' % data_proto)
