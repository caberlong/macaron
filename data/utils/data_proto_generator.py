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
      self._data = data
      self._scopes = []
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

    def _getProtoPathFields(self, parent, field_names:list, is_all:bool, results:list):
      """A Recursive function to return all fields with the field name list.

         is_all: if set true, returns all contents in repeated fields. Will not create any
                 new field if repeated field is empty.
                 if set false, create a new message for repeated fields if they are empty or the
                 field name is in 'self._new_repeats'. Returns the last one in the repeated fields. 
      """
      if not field_names:
        results.append(parent)
        return
      field_name = field_names[0]
      field = getattr(parent, field_name)
      field_descriptor = parent.DESCRIPTOR.fields_by_name[field_name]
      if field_descriptor.label == descriptor.FieldDescriptor.LABEL_REPEATED:
        if is_all:
          for f in field:
            self._getProtoPathFields(f, field_names[1:], is_all, results)
          return
        if not len(field) or (self._new_repeats and field_name in self._new_repeats):
          message = message_factory.MessageFactory().GetPrototype(field_descriptor.message_type)()  
          field.append(message)
        self._getProtoPathFields(field[-1], field_names[1:], is_all, results)
      else:
        self._getProtoPathFields(field, field_names[1:], is_all, results)

    def getProtoPathFields(self, parent, field_names:list, is_all:bool, results:list):
      self._getProtoPathFields(parent, field_names, is_all, results)

    def setFieldValue(self, parent, field_name, value):
      field_descriptor = parent.DESCRIPTOR.fields_by_name[field_name]
      if self.IsIntType(field_descriptor.type):
        setattr(parent, field_name, int(value))
      elif self.IsFloatType(field_descriptor.type):
        setattr(parent, field_name, float(value))
      else:
        setattr(parent, field_name, value)

    def assignFieldValue(
        self, parent, scopes:list, proto_path:DataGeneratorParser.ProtoPathContext, value):
      field_names = []
      field_names.extend(scopes)
      pp = proto_path
      while pp.protoPath():
        field_names.append(pp.NAME().getText())
        pp = pp.protoPath()
      results = []
      self.getProtoPathFields(self._data, field_names, is_all=False, results=results)
      assert len(results) == 1
      self.setFieldValue(results[0], pp.NAME().getText(), value)

    def pushScope(self, field_name):
      """push the field message as the current scope."""
      self._scopes.append(field_name)

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
      proto_path = refVar.protoPath().protoPath()
      if proto_path == None:
        return result
      fields = [];
      while proto_path:
        fields.append(proto_path.NAME().getText())
        proto_path = proto_path.protoPath()
      results = [];
      self.getProtoPathFields(result, fields, is_all=True, results=results)
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
      value = self.evalExpr(ctx.expr())
      if isinstance(value, list):
        for v in value:
          self.assignFieldValue(self._data, self._scopes, ctx.protoPath(), v)
      else:
        self.assignFieldValue(self._data, self._scopes, ctx.protoPath(), value)

                                                                                                    
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
