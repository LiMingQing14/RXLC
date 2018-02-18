#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

__all__ = ['traverse', 'getFileJson']

import FileInfo as FI
import FileConfig as FC
import FileHandle as FH

def traverse(directory_tuple, prefix_tuple):
    """"""
    assets = {}
    for name in directory_tuple:
        prefix = prefix_tuple[directory_tuple.index(name)]
        for (root, dirs, files) in os.walk(name):
            for file_name in files:
                file_info = FI.FileInfo(os.path.join(root, file_name), prefix)
                key, value = file_info.getAsset()
                assets[key] = value
    return assets

def getFileJson(root = '.', is_version_add = False):
    """"""
    json = {}
    json["version"] = _GetVersionCode()
    json['assets'] = _GetAssets(root)

    if is_version_add:
        _SetVersionCode(json["version"] + 1)

    return json

def _GetVersionCode():
    """获取版本号"""
    return int(FH.readFile(FC.getVersionCodeCfg()))

def _SetVersionCode(version_code):
    """设置版本号"""
    FH.writeFile(FC.getVersionCodeCfg(), str(version_code))

def _GetAssets(root):
    """"""
    # 当前工作目录
    cwd = os.getcwd()

    # 切换到指定目录
    os.chdir(root)

    """遍历指定文件夹下的所有文件"""
    dir_tuple, pre_tuple = FC.getHotUpdateDirectoryCfg()
    assets = traverse(dir_tuple, pre_tuple)

    # 切回原工作目录
    os.chdir(cwd)
    return assets

if __name__ == '__main__':
    print _GetAssets('../..')
