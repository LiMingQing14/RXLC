#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import json
import os
import shutil

import Helper

__all__ = ['HotUpdate', 'Project']

VERSION_CODE = 'version_code'

# key in Asset
SIZE = 'size'
MD5 = 'md5'
OLD = 'old'
# key in Assets
pass
# key in Project
VERSION = 'version'
ASSETS = 'assets'


Config = None
def setConfig(config):
    """设置常量配置"""
    global Config
    Config = config

def getFileMD5(file_name):
    """获取文件的MD5"""
    buff_size = 8192 # 读取buff大小
    md5_obj = hashlib.md5()
    f = file(file_name, 'rb')
    while True:
        buff = f.read(buff_size)
        if not buff:
            break
        md5_obj.update(buff)
    f.close()
    return str(md5_obj.hexdigest()).upper()

def search(assets, folder_list):
    """遍历文件夹检索文件"""
    for name in folder_list:
        for (root, dirs, files) in os.walk(name):
            for file_name in files:
                asset = Asset()
                asset.update(os.path.join(root, file_name))
                assets.append(asset)

class Asset(object):
    """文件信息"""
    def __init__(self):
        super(Asset, self).__init__()
        self.__file = None
        self.__md5 = None
        self.__size = None
        self.__old = None

    def update(self, file):
        # 统一使用斜杠
        file = file.replace('\\', '/')

        # key
        self.file = file
        # value
        self.md5 = getFileMD5(file)
        self.size = os.path.getsize(file)

    @property
    def file(self):
        return self.__file

    @file.setter
    def file(self, file):
        self.__file = file

    @property
    def md5(self):
        return self.__md5

    @md5.setter
    def md5(self, md5):
        self.__md5 = md5

    @property
    def size(self):
        return self.__size

    @size.setter
    def size(self, size):
        self.__size = size

    @property
    def old(self):
        return self.__old

    @old.setter
    def old(self, old):
        self.__old = old

    def same(self, other):
        """判断是否与另一个Asset(other)"""
        return self == other or (self.file == other.file and self.md5 == other.md5)

    def toDict(self):
        ret = {}
        ret[SIZE] = self.size
        ret[MD5] = self.md5
        if isinstance(self.old, int):
            # 可能的老版本内
            ret[OLD] = self.old
        return ret

    @classmethod
    def toObj(cls, pairs):
        if not pairs.has_key(SIZE) or not pairs.has_key(MD5):
            # 不属于Asset
            return None
        asset = cls()
        asset.size = pairs[SIZE]
        asset.md5 = pairs[MD5]
        if pairs.has_key(OLD):
            asset.old = pairs[OLD]
        return asset

class Assets(object):
    """"""
    def __init__(self):
        super(Assets, self).__init__()
        # 列表存放所有文件数据
        self.__list = []

    def __iter__(self):
        return self.__list.__iter__()

    def __nonzero__(self):
        return True

    def __len__(self):
        return self.__list.__len__()

    def __getitem__(self, index):
        return self.__list[index]

    def __setitem__(self, index, item):
        self.__list[index] = item

    def __getattr__(self, name):
        return getattr(self.__list, name)

    def sort(self):
        # 以元素的关键值(file)排序
        self.__list.sort(key = lambda x: x.file)

    def contain(self, asset):
        """判断是否包含有这个asset"""
        for x in self.__list:
            if x.same(asset):
                return True
        return False

    def removeSame(self, other):
        """取出所有相同项"""
        # 先排序
        self.sort()
        other.sort()

        same_list = []
        # 按排序可优化遍历查找
        self_start, self_end = 0, len(self)
        other_start, other_end = 0, len(other)
        for x in xrange(self_start, self_end):
            for y in xrange(other_start, other_end):
                if self[x].same(other[y]):
                    same_list.append((x, y))
                    break

        return same_list

    def toDict(self):
        ret = {}
        for x in self.__list:
            ret[x.file] = x
        return ret

    @classmethod
    def toObj(cls, pairs):
        for x in pairs.values():
            if not isinstance(x, Asset):
                # 有任意一个不属于Asset
                return None
        assets = cls()
        for x, asset in pairs.items():
            asset.file = x
            assets.append(asset)
        return assets

class Project(object):
    """"""
    def __init__(self):
        super(Project, self).__init__()
        self.__version = None
        self.__assets = None

    def __repr__(self):
        return json.dumps(self, default=lambda obj: obj.toDict(), indent=4)

    @property
    def version(self):
        return self.__version

    @version.setter
    def version(self, version):
        self.__version = version

    @property
    def assets(self):
        return self.__assets

    @assets.setter
    def assets(self, assets):
        self.__assets = assets

    def compare(self, other):
        """比较两个project，得出差异项
        其中，first作为目标(destination)，second作为原始(source)
        差异是指first在second基础上的变化内容，变化：新增或修改，不包括缺失"""
        assets = Assets()
        for asset in self.assets:
            if other.assets.contain(asset):
                # 文件没有变化，忽略
                pass
            else:
                # 要么文件是新增的，要么文件内容被修改
                assets.append(asset)

        diff_project = Project()
        diff_project.version = self.version
        diff_project.assets = assets
        return diff_project

    @staticmethod
    def generate(root = '.', is_version_add = False):
        """"""
        assets = Assets()

        # 切到文件夹，并设置Assets
        cwd = os.getcwd()
        os.chdir(root)
        search(assets, Config['search_folder'])
        os.chdir(cwd)

        # 生成Project，并设置数据
        project = Project()
        project.version = int(Helper.readFile(VERSION_CODE))
        project.assets = assets

        if is_version_add:
            # 版本提升
            Helper.writeFile(VERSION_CODE, str(project.version + 1))

        return project

    def toDict(self):
        ret = {}
        ret[VERSION] = self.version
        ret[ASSETS] = self.assets
        return ret

    @classmethod
    def toObj(cls, pairs):
        if not pairs.has_key(VERSION) or not pairs.has_key(ASSETS):
            # 不属于Project
            return None
        project = cls()
        project.version = pairs.get(VERSION)
        project.assets = pairs.get(ASSETS)
        return project

    @staticmethod
    def load(path, **kw):
        """从文件中加载，并转化为Project对象"""
        kw['object_hook'] = lambda pairs: Asset.toObj(pairs) or Assets.toObj(pairs) or Project.toObj(pairs)
        with open(path, 'rb') as json_file:
            return json.load(json_file, **kw)

    def save(self, path, **kw):
        """保存Project，转成json"""
        kw['default'] = lambda obj: obj.toDict()
        kw['indent'] = 4
        with open(path, 'wb') as json_file:
            json.dump(self, json_file, **kw)

class HotUpdate(object):
    """"""
    def __init__(self, project, path):
        super(HotUpdate, self).__init__()
        self.__project = project

        # 确保有REMOTE文件夹
        if not os.path.exists(path):
            os.mkdir(path)
        Helper.pushd(path)

    def __del__(self):
        Helper.popd()

    @property
    def project(self):
        return self.__project

    def keepLasestDiff(self, origin_version):
        """"""
        project = self.project
        latest_assets = Assets()

        prev_version = project.version - 1
        while prev_version >= origin_version: # 若所有版本都比较完毕，停止查找
            # 对应的版本文件夹
            prev_folder = 'v' + str(prev_version)
            assert os.path.exists(prev_folder), u"[Error] 版本文件丢失（%s）" % prev_folder

            # 读取前一个project
            prev_project = Project.load(os.path.join(prev_folder, 'project.manifest'))
            prev_assets = prev_project.assets

            # 当前差异文件是否在旧的版本内？有就找出来
            same_list = project.assets.removeSame(prev_assets)
            # 设置为对应的旧版本号
            for x, y in same_list:
                project.assets[x].old = prev_assets[y].old
            # 从旧表移除，添加到新表
            latest_assets.extend([project.assets[x[0]] for x in same_list])

            # 是否还有文件未找到
            if len(project.assets) > 0:
                # 继续前一个版本
                prev_version = prev_version - 1
            else:
                # 全部找齐，结束
                break

        # 没有查找到的差异，认为是新的差异文件
        if len(project.assets) > 0:
            latest_assets.extend(project.assets)

        project.assets = latest_assets

    def create(self):
        self.__createVersion()
        self.__createProject()

    def __createVersion(self):
        """创建版本文件"""
        version_manifest = {}
        version_manifest['app_version'] = Config['app_version']
        version_manifest['major_version'] = 0
        version_manifest['minor_version'] = self.project.version

        for x in Config['pkg_list']:
            if not os.path.exists(x):
                os.mkdir(x)
            Helper.writeJson(os.path.join(x, 'version.manifest'), version_manifest)

    def __createProject(self):
        """创建热更文件与配置清单"""
        version = self.project.version
        folder = 'v' + str(version)

        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)

        # 遍历所有差异文件，将新的差异提取出来
        for asset in self.project.assets:
            if not asset.old or asset.old == version:
                # 不在旧版本内，或者就是当前版本，表示是新的差异文件
                src = os.path.join(Config['client'], asset.file)
                dst = os.path.join(folder, asset.file)
                Helper.copyFile(src, dst)
                # 额外复制一份到'all'文件夹
                dst = os.path.join('all', asset.file)
                Helper.copyFile(src, dst)
        # 保存配置清单
        self.project.save(os.path.join(folder, 'project.manifest'))

if __name__ == '__main__':
    os.chdir('..')

    def test1():
        project = Project.generate('..', False)
        project.save('local.json')

    def test2():
        project = Project.load('local.json')
        project.save('local.json')

    def test3():
        print Project.load(os.path.join('remote/v1', 'project.manifest'))

    # test1()
    # test2()
    test3()