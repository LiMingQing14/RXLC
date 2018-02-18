#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xTools import FileHandle, FileConfig, GetFileJson

if __name__ == '__main__':
    # 文件信息
    json = GetFileJson.getFileJson('..', False)

    # 保存文件
    FileHandle.writeJson(FileConfig.getLocalSaveCfg(), json)
