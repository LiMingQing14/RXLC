#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os

class FileInfo:
    """文件信息"""

    # 读取buff大小
    buff_size = 8192

    def __init__(self, file_name, prefix):
        self.file_name = file_name
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
        key = self.file_name.replace('\\', '/')
        element = key.split('/')
        element[0] = self.prefix # 修改前缀
        key = '/'.join(element)
        #
        value = {}
        value["File"] = self.file_name
        value['MD5'] = self._GetFileMD5()
        value['Size'] = self._GetFileSize()
        #
        return key, value
