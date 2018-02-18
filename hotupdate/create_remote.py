#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import shutil

from xTools import FileHandle, FileHelper, FileConfig, FileInfo, GetFileJson

REMOTE = 'remote'
PROJECT_MANIFEST = 'project.manifest'

def compareJson(local_json, remote_json):
    diff_json = {}
    diff_json['version'] = remote_json['version']
    diff_json['assets'] = {}

    local_assets = local_json['assets']
    remote_assets = remote_json['assets']
    diff_assets = diff_json['assets']
    for x in remote_assets:
        if local_assets.has_key(x):
            # 文件都有
            if local_assets[x][FileInfo.INFO_MD5] == remote_assets[x][FileInfo.INFO_MD5]:
                # 文件一致
                pass
            else:
                diff_assets[x] = remote_assets[x]
        else:
            diff_assets[x] = remote_assets[x]
    return diff_json

def comparePrevDiff(diff_json):
    """"""
    version = diff_json['version']
    prev_version = version - 1
    prev_folder = 'v' + str(prev_version)

    if os.path.exists(prev_folder):
        # 读取前一个json
        prev_json = FileHandle.readJson(os.path.join(prev_folder, PROJECT_MANIFEST))
        prev_asset = prev_json['assets']
        #
        diff_assets = diff_json['assets']
        for x in diff_assets:
            if prev_asset.has_key(x):
                if prev_asset[x][FileInfo.INFO_MD5] == diff_assets[x][FileInfo.INFO_MD5]:
                    diff_assets[x][FileInfo.INFO_SUB_VERSION] = prev_version

    return diff_json

def createVersion(file_json):
    """"""
    version = file_json['version']
    folder = 'v' + str(version)

    if os.path.exists(folder):
        shutil.rmtree(folder)
    os.mkdir(folder)

    # 遍历所有差异文件，将新的差异提取出来
    assets = file_json['assets']
    for x in assets:
        asset = assets[x]
        if not asset.has_key(FileInfo.INFO_SUB_VERSION) or asset[FileInfo.INFO_SUB_VERSION] == version:
            # 不存在子版本号，或者子版本号相同，表示是新的差异文件
            src = os.path.join('../..', asset[FileInfo.INFO_FILE])
            dst = os.path.join(folder, x)
            # 复制到新
            FileHelper.copyFile(src, dst)

    FileHandle.writeJson(os.path.join(folder, PROJECT_MANIFEST), file_json)

if __name__ == '__main__':
    # local与remote的json
    local_json = FileHandle.readJson(FileConfig.getLocalSaveCfg())
    remote_json = GetFileJson.getFileJson('..', True)
    # 比较两个json，得到差异表
    diff_json = compareJson(local_json, remote_json)

    # 确保有REMOTE文件夹
    if not os.path.exists(REMOTE):
        os.mkdir(REMOTE)

    # 切工作目录
    FileHelper.pushd(REMOTE)

    # 比较前一个hotupdate
    diff_json = comparePrevDiff(diff_json)
    # 创建json
    createVersion(diff_json)

    # 退出目录
    FileHelper.popd()
