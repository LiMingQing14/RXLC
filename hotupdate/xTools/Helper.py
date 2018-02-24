#!/usr/bin/env python
# -*- coding: utf-8 -*-

import copy
import json
import os
import shutil

__all__ = [
    'pushd', 'popd',
    'readJson', 'writeJson', 'readFile', 'writeFile',
    'copyFile', 'shallowCopy', 'deepCopy',
]

_cwd = '.'

def pushd(dir):
    """地址入栈"""
    global _cwd
    _cwd = os.getcwd()
    os.chdir(dir)

def popd():
    """地址出栈"""
    global _cwd
    os.chdir(_cwd)

def readJson(path):
    """读取Json文件"""
    with open(path, 'r') as json_file:
        return json.load(json_file)

def writeJson(path, data):
    """保存为Json文件"""
    with open(path, 'w+') as json_file:
        json.dump(data, json_file, indent=4)

def readFile(path):
    """读取文件"""
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def writeFile(path, content):
    """保存文件"""
    f = open(path, "w+")
    f.write(content)
    f.close()

def copyFile(src, dst):
    """文件拷贝"""
    # 确保文件夹存在
    path = os.path.split(dst)[0]
    if not os.path.exists(path):
        os.makedirs(path)
    # 复制文件
    shutil.copyfile(src, dst)

def shallowCopy(var):
    """浅复制"""
    return copy.copy(var)

def deepCopy(var):
    """深复制"""
    return copy.deepcopy(var)