from setuptools import setup

APP = ['server.py']  # 你的主脚本
OPTIONS = {
    'argv_emulation': True,
    'packages': ['rubicon', 'rubicon.objc'],  # 👈 显式加入
    'includes': ['rubicon.objc'],
}

setup(
    app=APP,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
