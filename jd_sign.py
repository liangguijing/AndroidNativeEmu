# -*- coding: utf-8 -*-
"""
Author  : Jack.Liang
Time    : 2021/8/20 17:58
"""

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


# Initialize emulator
emulator = Emulator(
    vfs_root=posixpath.join(posixpath.dirname(__file__), "vfs")
)

lib_module = emulator.load_library("jd_so/libjdbitmapkit.so", do_init=False)


def get_sign(function_id, body_string, uuid, platform, version):
    try:
        # Run JNI_OnLoad.
        #   JNI_OnLoad will call 'RegisterNatives'.
        # emulator.call_symbol(lib_module, 'JNI_OnLoad', emulator.java_vm.address_ptr, 0x00)
        activity_Th = ActivityThread()
        str1 = String(function_id)
        str2 = String(body_string)
        str3 = String(uuid)
        str4 = String(platform)
        str5 = String(version)
        result = emulator.call_symbol(lib_module, 'Java_com_jingdong_common_utils_BitmapkitUtils_getSignFromJni',
                                      emulator.java_vm.jni_env.address_ptr, 0x00, activity_Th.getSystemContext(emulator),
                                      str1, str2, str3, str4, str5
                                      )
        print(result)
        print(type(result), result.get_py_string())
    except UcError as e:
        print("Exit at %x" % emulator.mu.reg_read(UC_ARM_REG_PC))
        raise


get_sign("1", "1", "1", "1", "1", )
