#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from xTools import *

LOCAL_JSON = 'local.json'

if __name__ == '__main__':
    # 文件信息
    project = Project.generate(Config['client'], False)
    # 保存文件
    project.save(LOCAL_JSON)
