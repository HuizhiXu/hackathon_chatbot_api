"""
-*- coding: UTF-8 -*-
@Time : 2023/3/21  19:10
@Description :
@Author : Huizhi XU
"""

import configparser
import os.path

# Open a configuration file
config = configparser.ConfigParser()
file_path = os.path.dirname(os.path.abspath('.')) + 'config.ini' #返回上级目录再访问某文件（路径根据实际情况自定义）
config.read(file_path)
open_ai_key = str(config.get("open_ai", "OPENAI_API_KEY"))
serapi_key = str(config.get("serp_api", "SERPAPI_API_KEY"))

