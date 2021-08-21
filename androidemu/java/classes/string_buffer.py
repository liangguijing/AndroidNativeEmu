from ..java_class_def import JavaClassDef
from ..java_field_def import JavaFieldDef
from ..java_method_def import java_method_def, JavaMethodDef
from .array import Array
from .string import String


class StringBuffer(metaclass=JavaClassDef, jvm_name='java/lang/StringBuffer'):
    
    def __init__(self):
        self._list = []

    @java_method_def(name='<init>', signature='()V', native=False)
    def new(self, emu):
        return self

    @java_method_def(name='append', args_list=["jstring"],
                     signature='(Ljava/lang/String;)Ljava/lang/StringBuffer;', native=False)
    def append(self, emu, arg):
        self._list.append(String(arg))
        return self

    @java_method_def(name='toString', args_list=[],
                     signature='()Ljava/lang/String;', native=False)
    def to_string(self, emu):
        s = ""
        for i in self._list:
            s += str(i)
        return String(s)

    def __repr__(self):
        return "JavaStringBuffer(%s)" % self.to_string()
