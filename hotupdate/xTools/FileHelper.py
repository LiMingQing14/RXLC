#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy as cpy
import os
import shutil

__all__ = ['pushd', 'popd', 'getPrevCwd', 'copyFile']

cwd = '.'

def pushd(dir):
    global cwd
    cwd = os.getcwd()
    os.chdir(dir)

def popd():
    global cwd
    os.chdir(cwd)

def getPrevCwd():
    return cwd

def copyFile(src, dst):
    # 确保文件夹存在
    path = os.path.split(dst)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    # 复制文件
    shutil.copyfile(src, dst)

def shallowCopy(var):
    """浅复制"""
    return cpy.copy(var)

def deepCopy(var):
    """深复制"""
    return cpy.deepcopy(var)