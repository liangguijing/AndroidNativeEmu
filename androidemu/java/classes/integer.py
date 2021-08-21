
from ..java_class_def import JavaClassDef
from ..java_field_def import JavaFieldDef
from ..java_method_def import java_method_def, JavaMethodDef
from .string import String


class Integer(metaclass=JavaClassDef, jvm_name='java/lang/Integer'):
    def __init__(self):
        self._int = None

    @java_method_def(name='<init>', args_list=["jint"], signature='(I)V', native=False)
    def new(self, emu, i):
        self._int = i

    @java_method_def(name='toString', args_list=[],
                     signature='()Ljava/lang/String;', native=False)
    def to_string(self, emu):
        return String(self._int)

    def __repr__(self):
        return "JavaInteger(%s)" % str(self._int)
