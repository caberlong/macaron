import sys
from antlr4 import *
from DataGeneratorLexer import DataGeneratorLexer
from DataGeneratorParser import DataGeneratorParser
from DataGeneratorParserListener import DataGeneratorParserListener
from proto import data_pb2
from google.protobuf import message_factory
from google.protobuf import descriptor


class DataProtoGenerator:
  def __init__(self):
    pass

  class Listener(DataGeneratorParserListener):
    def __init__(self, data: data_pb2.Data, new_repeats: dict=None, var_values: dict={}):
      self._scopes = [data]
      self._var_values = var_values
      # overwrite the last instead of append a new one for repeated fields.
      self._new_repeats = new_repeats

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

    def getProtoPathFields(self, parent, ctx:DataGeneratorParser.ProtoPathContext, results:list):
      if ctx.protoPath() == None:
        results.append((parent, ctx.NAME().getText()))
        return
      field_name = ctx.NAME().getText()
      field = getattr(parent, field_name)
      field_descriptor = parent.DESCRIPTOR.fields_by_name[field_name]
      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        for f in field:
          self.getProtoPathFields(f, ctx.protoPath(), results)
      else:
        self.getProtoPathFields(field, ctx.protoPath(), results)

    def setFieldValue(self, parent, field_name, value):
      field_descriptor = parent.DESCRIPTOR.fields_by_name[field_name]
      if self.IsIntType(field_descriptor.type):
        setattr(parent, field_name, int(value))
      elif self.IsFloatType(field_descriptor.type):
        setattr(parent, field_name, float(value))
      else:
        setattr(parent, field_name, value)

    def pushScope(self, field_name):
      """push the field message as the current scope."""
      field = getattr(self._scopes[-1], field_name)
      field_descriptor = self._scopes[-1].DESCRIPTOR.fields_by_name[field_name]
      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        if not len(field) or (self._new_repeats and field_name in self._new_repeats): 
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
      result = self._var_values[refVar.protoPath().NAME().getText()]
      if refVar.protoPath().protoPath() == None:
        return result
      fields = [];
      self.getProtoPathFields(result, refVar.protoPath().protoPath(), fields)
      results = [];
      for parent, field_name in fields:
        results.append(getattr(parent, field_name))
      if len(results) == 1:
        return results[0]
      return results

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
    def enterAssignField(self, ctx:DataGeneratorParser.AssignFieldContext):
      fields = []
      self.getProtoPathFields(self._scopes[-1], ctx.protoPath(), fields)
      assert len(fields) == 1
      (parent, field_name) = fields[0]
      self.setFieldValue(parent, field_name, self.evalExpr(ctx.expr()))
                                                                                                    
  def generateDataProto(
      self, config: str, data: data_pb2.Data, new_repeats: dict=None, var_values: dict={}):
    """new_repeats: repeat fields that need to be newly created."""
    lexer = DataGeneratorLexer(InputStream(config))
    stream = CommonTokenStream(lexer)
    parser = DataGeneratorParser(stream)
    tree = parser.generateDataProto()
    walker = ParseTreeWalker();
    listener = self.Listener(data=data, new_repeats=new_repeats, var_values=var_values);
    walker.walk(listener, tree);
