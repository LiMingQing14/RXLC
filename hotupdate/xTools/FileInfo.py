#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

INFO_FILE = 'file'
INFO_MD5 = 'md5'
INFO_SIZE = 'size'
INFO_SUB_VERSION = 'sub_version'

class FileInfo:
    """文件信息"""

    # 读取buff大小
    buff_size = 8192

    def __init__(self, file_name, prefix):
        self.file_name = file_name.replace('\\', '/')
        self.prefix = prefix

    def _GetFileMD5(self):
        """获取文件的MD5"""
        md5_obj = hashlib.md5()
        f = file(self.file_name, 'rb')
        while True:
            buff = f.read(FileInfo.buff_size)
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
        value[INFO_FILE] = self.file_name
        value[INFO_MD5] = self._GetFileMD5()
        value[INFO_SIZE] = self._GetFileSize()
        #
        return key, value
