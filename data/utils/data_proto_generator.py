import sys
from antlr4 import *
from DataGeneratorLexer import DataGeneratorLexer
from DataGeneratorParser import DataGeneratorParser
from DataGeneratorParserListener import DataGeneratorParserListener
from data.proto import data_pb2
from google.protobuf import message_factory
from google.protobuf import descriptor


class DataProtoGenerator:
  def __init__(self):
    pass

  class Listener(DataGeneratorParserListener):
    def __init__(self, data: data_pb2.Data, overwrite: bool=None, var_values: dict={}):
      self._scopes = [data]
      self._proto_paths = []
      self._var_values = var_values
      # overwrite the last instead of append a new one for repeated fields.
      self._overwrite = overwrite

    def IsIntType(self, field_type):
      return (field_type == descriptor.FieldDescriptor.TYPE_INT64 or
          field_type == descriptor.FieldDescriptor.TYPE_UINT64 or
          field_type == descriptor.FieldDescriptor.TYPE_INT32 or
          field_type == descriptor.FieldDescriptor.TYPE_FIXED64 or
          field_type == descriptor.FieldDescriptor.TYPE_FIXED32 or
          field_type == descriptor.FieldDescriptor.TYPE_UINT32 or
          field_type == descriptor.FieldDescriptor.TYPE_SFIXED32 or
          field_type == descriptor.FieldDescriptor.TYPE_SFIXED64 or
          field_type == descriptor.FieldDescriptor.TYPE_SINT32 or
          field_type == descriptor.FieldDescriptor.TYPE_SINT64)

    def IsFloatType(self, field_type):
      return (field_type == descriptor.FieldDescriptor.TYPE_FLOAT or
          field_type == descriptor.FieldDescriptor.TYPE_DOUBLE)

    def setFieldValue(self, value):
      scope_field = self._scopes[-1]
      for path in self._proto_paths[:-1]:
        scope_field = getattr(scope_field, path)

      field_name = self._proto_paths[-1]
      field_descriptor = scope_field.DESCRIPTOR.fields_by_name[field_name]
      if self.IsIntType(field_descriptor.type):
        setattr(scope_field, field_name, int(value))
      elif self.IsFloatType(field_descriptor.type):
        setattr(scope_field, field_name, float(value))
      else:
        setattr(scope_field, field_name, value)

    def pushScope(self, field_name):
      """push the field message as the current scope."""
      field = getattr(self._scopes[-1], field_name)
      field_descriptor = self._scopes[-1].DESCRIPTOR.fields_by_name[field_name]
      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        if not len(field) or not self._overwrite: 
          message = message_factory.MessageFactory().GetPrototype(field_descriptor.message_type)()
          getattr(self._scopes[-1], field_name).append(message)
        self._scopes.append(field[-1])
        return
      self._scopes.append(field)
          
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

  def generateDataProto(
      self, config: str, data: data_pb2.Data, overwrite: bool=None, var_values: dict={}):
    lexer = DataGeneratorLexer(InputStream(config))
    stream = CommonTokenStream(lexer)
    parser = DataGeneratorParser(stream)
    tree = parser.generateDataProto()
    walker = ParseTreeWalker();
    listener = self.Listener(data=data, overwrite=overwrite, var_values=var_values);
    walker.walk(listener, tree);
