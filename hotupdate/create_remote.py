#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from xTools import *

LOCAL_JSON = 'local.json'
REMOTE = 'remote'

if __name__ == '__main__':
    if not os.path.exists(LOCAL_JSON):
        print(u'[Warning] 本地的"%s"并未生成，请先执行"local.py"！' % LOCAL_JSON)
        os.system('pause')
        exit()

    """ 第二步：读取当前最新文件的配置，然后与原始配置比较，得到当前热更的差异配置 """
    # local与remote的project
    local_project = Project.load(LOCAL_JSON)
    remote_project = Project.generate(Config['client'], False)
    # 比较两个project，得到差异表
    diff_project = remote_project.compare(local_project)

    """ 第三步：优化差异，生成差异配置与热更版本内容 """
    # 开始热更（进入路径）
    hotupdate = HotUpdate(diff_project, REMOTE)
    # 取出最新的热更（避免重复旧的热更）
    hotupdate.keepLasestDiff(local_project.version)
    print hotupdate.project
    # 完成热更的文件创建
    hotupdate.create()
    # 退出热更（路径恢复）
    del hotupdate

    print(u'[Finish] 成功生成热更配置，当前版本为%d。' % diff_project.version)
    # os.system('pause')
    exit()
