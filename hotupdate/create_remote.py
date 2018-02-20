#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ConfigParser
import os
import shutil

from xTools import FileHandle, FileHelper, FileConfig, FileInfo, GetFileJson

REMOTE = 'remote'
PROJECT_MANIFEST = 'project.manifest'
SETTING_INI = 'setting.ini'

config_data = {}

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
            if local_assets[x][FileInfo.MD5] == remote_assets[x][FileInfo.MD5]:
                # 文件一致
                pass
            else:
                diff_assets[x] = remote_assets[x]
        else:
            diff_assets[x] = remote_assets[x]
    return diff_json

def comparePrevDiff(diff_json, start_version):
    """"""
    version = diff_json['version']
    diff_assets = diff_json['assets']

    new_asset = {}

    prev_version = version - 1
    while prev_version >= start_version: # 所有版本都比较完毕
        # 对应的版本文件夹
        prev_folder = 'v' + str(prev_version)
        assert os.path.exists(prev_folder), u"Error: 版本文件丢失（%s）" % prev_folder

        # 读取前一个json
        prev_json = FileHandle.readJson(os.path.join(prev_folder, PROJECT_MANIFEST))
        assert prev_version == prev_json['version'], u"Error: 版本号不一致（%d %d）" % (prev_version, prev_json['version'])
        prev_asset = prev_json['assets']

        # 当前差异文件是否在旧的版本内？
        pop_list = []
        for name, asset in diff_assets.items():
            if prev_asset.has_key(name) and prev_asset[name][FileInfo.MD5] == asset[FileInfo.MD5]:
                # 设置为子版本号或当前版本号
                asset[FileInfo.SUB_VERSION] = prev_asset[name].get(FileInfo.SUB_VERSION, prev_version)
                # 标识为要删除
                pop_list.append(name)

        # 从旧表移除，添加到新表
        for name in pop_list:
            new_asset[name] = diff_assets.pop(name)

        # 是否还有文件未找到
        if len(diff_assets) > 0:
            # 继续前一个版本
            prev_version = prev_version - 1
        else:
            # 全部找齐，结束
            break

    # 没有查找到的差异，认为是新的差异文件
    if len(diff_assets) > 0:
        for name, asset in diff_assets.items():
            new_asset[name] = asset

    new_json = {}
    new_json['version'] = version
    new_json['assets'] = new_asset
    return new_json

def createVersion(file_json):
    def replace(matched):
        return str(config_data[matched.group('value')])
    import re
    content = FileHandle.readFile('../version_template')
    content = re.sub('{p(?P<value>\w+)}', replace, content)
    for x in config_data['pkg_list']:
        if not os.path.exists(x):
            os.mkdir(x)
        FileHandle.writeFile(os.path.join(x, 'version.manifest'), content)

def createProject(file_json):
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
        if not asset.has_key(FileInfo.SUB_VERSION) or asset[FileInfo.SUB_VERSION] == version:
            # 不存在子版本号，或者子版本号相同，表示是新的差异文件
            src = os.path.join('../..', asset[FileInfo.FILE])
            dst = os.path.join(folder, x)
            # 复制到新
            FileHelper.copyFile(src, dst)

def saveProjectManifest(file_json):
    version = file_json['version']
    folder = 'v' + str(version)

    save_json = FileHelper.deepCopy(file_json)
    for x in save_json['assets']:
        asset = save_json['assets'][x]
        if asset.has_key(FileInfo.FILE):
            del asset[FileInfo.FILE]
    FileHandle.writeJson(os.path.join(folder, PROJECT_MANIFEST), save_json)

def initSetting():
    parser = ConfigParser.ConfigParser(allow_no_value = True)
    parser.read(SETTING_INI)

    config_data['app_version'] = parser.getint('default', 'app_version')
    config_data['pkg_list'] = {}
    for x in parser.options('pkg_list'):
        data = {}
        data['name'] = parser.get(x, 'name')
        data['enable_update'] = parser.getboolean(x, 'enable_update')
        data['enable_debug'] = parser.getboolean(x, 'enable_debug')
        config_data['pkg_list'][x] = data

    config_data[]

    del parser

if __name__ == '__main__':
    initSetting()

    # local与remote的json
    local_json = FileHandle.readJson(FileConfig.getLocalSaveCfg())
    remote_json = GetFileJson.getFileJson('..', False)
    # 比较两个json，得到差异表
    diff_json = compareJson(local_json, remote_json)

    config_data['version'] = remote_json['version']

    # 确保有REMOTE文件夹
    if not os.path.exists(REMOTE):
        os.mkdir(REMOTE)

    # 切工作目录
    FileHelper.pushd(REMOTE)

    # 比较前一个hotupdate
    start_version = local_json['version']
    diff_json = comparePrevDiff(diff_json, start_version)
    # 创建版本文件
    createVersion(diff_json)
    # 创建热更文件
    createProject(diff_json)
    # 保存热更文件清单
    saveProjectManifest(diff_json)

    # 退出目录
    FileHelper.popd()
