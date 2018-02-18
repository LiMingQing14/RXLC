#!/usr/bin/env python
# -*- coding: utf-8 -*-

from xTools import FileHandle, FileConfig, GetFileJson

def compareJson(local_json, remote_json):
    diff_json = {}
    diff_json['version'] = remote_json['version']
    diff_json['assets'] = {}

    local_assets = local_json['assets']
    remote_assets = remote_assets['assets']
    diff_assets = diff_json['assets']
    for x in remote_assets:
        if local_assets.has_key(x):
            # 文件都有
            if local_assets[x]['MD5'] == remote_assets[x]['MD5']:
                # 文件一致
                pass
            else:
                diff_assets[x] = remote_assets[x]
        else:
            diff_assets[x] = remote_assets[x]
    return diff_json

def comparePrevDiff(diff_json):
    version = diff_json['version']
    prev_version = version - 1
    if os.path.isexist():
        pass
    return diff_json

if __name__ == '__main__':
    # 文件信息
    file_json = GetFileJson.getFileJson('..', True)

    # 保存文件
    # FileHandle.writeJson(FileConfig.getRemoteSaveCfg(), file_json)

    # local与remote的json
    local_json = FileHandle.readJson(FileConfig.getLocalSaveCfg())
    remote_json = file_json

    # 比较两个json，得到差异表
    diff_json = compareJson(local_json, remote_json)

    # 比较前一个hotupdate
    diff_json = comparePrevDiff(diff_json)

    # 创建json
