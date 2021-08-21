
import posixpath

from unicorn import *
from unicorn.arm_const import *

from androidemu.emulator import Emulator
from androidemu.java.classes.activity_thread import ActivityThread
from androidemu.java.classes.application import Application
from androidemu.java.java_class_def import JavaClassDef
from androidemu.java.java_method_def import java_method_def
from androidemu.java.java_field_def import JavaFieldDef
from androidemu.java.classes.string import String


class BitmapkitUtils(metaclass=JavaClassDef, jvm_name='com/jingdong/common/utils/BitmapkitUtils',
                     jvm_fields=[JavaFieldDef("a", "Landroid/app/Application;", True, Application())]):

    def __init__(self):
        pass

    @java_method_def(name='a', signature='([Ljava/lang/String;)Ljava/lang/String;', native=True)
    def a(self, mu, s):
        pass

    @java_method_def(name='encodeJni', signature='([BZ)[B', native=True)
    def encodeJni(self, mu):
        pass

    @java_method_def(
        name='getSignFromJni',
        args_list=['jobject', "jstring", "jstring", "jstring", "jstring", "jstring"],
        signature='(Landroid/content/Context;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;Ljava/lang/String;)Ljava/lang/String;',
        native=True)
    def getSignFromJni(self, mu, str1, str2, str3, str4, str5):
        pass

    @java_method_def(name='getstring', signature='(Ljava/lang/String;)Ljava/lang/String;', native=True)
    def getstring(self, mu):
        pass


# logger = logging.getLogger(__name__)
# logger = logging.getLogger()
# logger.setLevel(logging.ERROR)

# Initialize emulator
emulator = Emulator(
    vfs_root=posixpath.join(posixpath.dirname(__file__), "vfs")
)

emulator.java_classloader.add_class(BitmapkitUtils)
# Register Java class.
lib_module = emulator.load_library("jd_so/libjdbitmapkit.so", do_init=False)
# print(lib_module.symbols)
# emulator.mu.hook_add(UC_HOOK_CODE, hook_code, emulator)

# for module in emulator.modules:
#     logger.info("=> 0x%08x - %s" % (module.base, module.filename))


try:
    # Run JNI_OnLoad.
    #   JNI_OnLoad will call 'RegisterNatives'.
    # emulator.call_symbol(lib_module, 'JNI_OnLoad', emulator.java_vm.address_ptr, 0x00)
    activity_Th = ActivityThread()
    str1 = String("11")
    str2 = String("11")
    str3 = String("11")
    str4 = String("11")
    str5 = String("11")
    result = emulator.call_symbol(lib_module, 'Java_com_jingdong_common_utils_BitmapkitUtils_getSignFromJni',
                                  emulator.java_vm.jni_env.address_ptr, 0x00, activity_Th.getSystemContext(emulator),
                                  str1, str2, str3, str4, str5
                                  )
    print(result)
    print(type(result), result.get_py_string())
except UcError as e:
    print("Exit at %x" % emulator.mu.reg_read(UC_ARM_REG_PC))
    raise
