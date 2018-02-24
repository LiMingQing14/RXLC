
__version__ = '1.0.0'
__author__ = 'LiMingQing <LiMingQing14@gmail.com>'

__all__ = ['HotUpdate', 'Project', 'Config']

from .HotUpdate import HotUpdate, Project, setConfig

Config = None
############################################################

import os
import ConfigParser

SETTING_INI = 'setting.ini'

def setting():
    parser = ConfigParser.ConfigParser(allow_no_value = True)
    parser.read(SETTING_INI)

    config = {}

    # app version
    config['app_version'] = parser.getint('default', 'app_version')
    # client path
    config['client'] = os.path.abspath(os.path.join(os.getcwd(), parser.get('default', 'client')))
    # hotupdate's folders
    config['search_folder'] = parser.get('default', 'search_folder').split(',')
    # package name list
    config['pkg_list'] = {}
    for x in parser.options('pkg_list'):
        data = {}
        # name, enable_update, enable_debug
        data['name'] = parser.get(x, 'name')
        data['enable_update'] = parser.getboolean(x, 'enable_update')
        data['enable_debug'] = parser.getboolean(x, 'enable_debug')
        config['pkg_list'][x] = data

    del parser
    return config

if Config is None:
    Config = setting()

setConfig(Config)
