
class Field(object):
    def __init__(self, name=None, default=None, data_type=None):
        self.name = name
        self.default = default
        self.required = self.default is None
        self.type = data_type

    def build(self):
        result = {key: value for key, value in self.__dict__.items() if value is not None}
        if self.name is not None:
            del result["name"]
            result = {self.name: result}
        return result

class MultiField(object):
    def __init__(self, fields, name=None):
        self.fields = fields
        self.name = name

    def build(self):
        result = {}
        for i in self.fields:
            result.update(i.build())

        if self.name is None:
            return result
        else:
            return {self.name: result}

class TypeField(Field):
    data_type = None
    def __init__(self, name=None, default=None):
        super().__init__(name=name, default=default, data_type=self.data_type)

class IntegerField(TypeField):
    data_type = "integer"

class FloatField(TypeField):
    data_type = "float"

class StringField(TypeField):
    data_type = "string"

class BooleanField(TypeField):
    data_type = "boolean"

class ListField(object):

    def __init__(self, name, field=None):
        self.name = name
        if field is None:
            self.field = StringField()
        else:
            self.field = field
    def build(self):
        return {self.name: [self.field.build()]}


