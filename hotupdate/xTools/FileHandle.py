#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

def readJson(path):
    """读取Json文件"""
    with open(path, 'r') as json_file:
        return json.load(json_file)

def writeJson(path, data):
    """保存为Json文件"""
    with open(path, 'w+') as json_file:
        json.dump(data, json_file, encoding = 'utf-8', indent = 4)

def readFile(path):
    """读取文件"""
    f = open(path, "r")
    content = f.read()
    f.close()
    return content

def writeFile(path, content):
    """保存文件"""
    f = open(path, "w+")
    f.write(content)
    f.close()
