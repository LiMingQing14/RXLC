#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

FILE = 'file'
MD5 = 'md5'
SIZE = 'size'
SUB_VERSION = 'sub_version'

class Asset:
    """文件信息"""

    # 读取buff大小
    buff_size = 8192

    def __init__(self, file_name, prefix):
        file_name = file_name.replace('\\', '/')

        element = file_name.split('/')
        element[0] = prefix # 修改前缀文件夹名
        self.key = '/'.join(element)

        self.file_name = file_name
        self.md5 = self._GetFileMD5()
        self.size = self._GetFileSize()
        self.sub_version = 0

    def _GetFileMD5(self):
        """获取文件的MD5"""
        md5_obj = hashlib.md5()
        f = file(self.file_name, 'rb')
        while True:
            buff = f.read(Asset.buff_size)
            if not buff:
                break
            md5_obj.update(buff)
        f.close()
        return str(md5_obj.hexdigest()).upper()

    def _GetFileSize(self):
        """获取文件的大小（字节）"""
        return os.path.getsize(self.file_name)

    def getAsset(self):
        """
            获得文件信息，字典形式：
            key值是文件名（变换后），
            value值是文件MD5、大小与文件名（原）
        """
        # 名字
        element = self.file_name.split('/')
        element[0] = self.prefix # 修改前缀文件夹名
        key = '/'.join(element)
        #
        value = {}
        value[FILE] = self.file_name
        value[MD5] = self._GetFileMD5()
        value[SIZE] = self._GetFileSize()
        #
        return key, value

class Assets:
    def __init__()