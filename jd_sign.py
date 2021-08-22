# -*- coding: utf-8 -*-
"""
Author  : Jack.Liang
Time    : 2021/8/20 17:58
"""

import posixpath
import sys

from unicorn import *
from unicorn.arm_const import *

from androidemu.emulator import Emulator
from androidemu.java.classes.activity_thread import ActivityThread
from androidemu.java.classes.string import String


def hook_code(mu, address, size, user_data):
    global lib_module_base

    try:
        emu = user_data
        if (not emu.memory.check_addr(address, UC_PROT_EXEC)):
            print("addr 0x%08X out of range"%(address,))
            sys.exit(-1)

        # 修改gettimeofday返回值
        if (lib_module_base + 0x129C0) == address:
            # 读取R5寄存器的值
            r5 = mu.reg_read(UC_ARM_REG_R5)
            print(">>> addr 0x%08X,r5=0x%08X" % (address, r5))

            # 读取R5指向的内存地址的值，就是tv的值
            b = mu.mem_read(r5, 8).hex().upper()
            print(b)

            # 给 tv写入一个定值
            mu.mem_write(r5, b"\x91\x50\xc4\x5f\x15\x97\x09\x00")

            # 看一眼，是不是写对了
            b = mu.mem_read(r5, 8).hex().upper()
            print(b)

        # 修改 lrand48的返回值
        if (lib_module_base + 0x00012A72) == address or (lib_module_base + 0x00012A8C) == address:
            r0 = mu.reg_read(UC_ARM_REG_R0)
            print(">>> addr 0x%08X,r0=0x%08X" % (address, r0))
            mu.reg_write(UC_ARM_REG_R0, 1)
    except Exception as e:
        print(e)
        print("exception in hook_code")
        sys.exit(-1)


# Initialize emulator
emulator = Emulator(
    vfs_root=posixpath.join(posixpath.dirname(__file__), "vfs")
)

lib_module = emulator.load_library("so/libjdbitmapkit.so", do_init=False)
lib_module_base = lib_module.base
emulator.mu.hook_add(UC_HOOK_CODE, hook_code, emulator)


def get_sign(function_id, body_string, uuid, client, version):
    try:
        act_th = ActivityThread()
        function_id = String(function_id)
        body_string = String(body_string)
        uuid = String(uuid)
        client = String(client)
        version = String(version)
        result = emulator.call_symbol(lib_module, 'Java_com_jingdong_common_utils_BitmapkitUtils_getSignFromJni',
                                      emulator.java_vm.jni_env.address_ptr, 0x00, act_th.getSystemContext(emulator),
                                      function_id, body_string, uuid, client, version)
        print(result)
        return str(result)
    except UcError as e:
        print("Exit at %x" % emulator.mu.reg_read(UC_ARM_REG_PC))
        return ""


get_sign("1", "1", "1", "1", "1", )
