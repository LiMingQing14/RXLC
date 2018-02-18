#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os

# 配置文件名
CONFIG_INI = 'config.ini'

__all__ = ['getVersionCodeCfg', 'getHotUpdateDirectoryCfg']

# 配置解析器
__config_parser = None

def __LazyInit():
    """简单初始化解析器"""
    global __config_parser
    if not __config_parser:
        __config_parser = ConfigParser.ConfigParser(allow_no_value = True)

        directory = os.path.split(os.path.abspath(__file__))[0]
        __config_parser.read(os.path.join(directory, CONFIG_INI))

def getVersionCodeCfg():
    """获取版本号文件名字"""
    __LazyInit()
    options = __config_parser.options('VERSION')
    return options[0]

def getHotUpdateDirectoryCfg():
    """获取热更文件夹配置"""
    __LazyInit()
    items = __config_parser.items('DIRECTORY')

    dir_list, pre_list = [], []
    for prefix, folder in items:
        array = folder.split(',') # ','分隔
        for x in range(len(array)):
            pre_list.append(prefix)
        dir_list.extend(array)
    return tuple(dir_list), tuple(pre_list)

def getLocalSaveCfg():
    __LazyInit()
    return __config_parser.get('SAVE', 'local')

def getRemoteSaveCfg():
    __LazyInit()
    return __config_parser.get('SAVE', 'remote')

if __name__ == '__main__':
    print getVersionCodeCfg()
    print getHotUpdateDirectoryCfg()
