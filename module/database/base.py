#!/usr/bin/python3
import sqlite3


class Connect(object):
    def __init__(self):
        self.cx = None
        self.cu = None

    def __enter__(self):
        self.cx = sqlite3.connect('data.db')
        self.cu = self.cx.cursor()
        return self.cu

    def __exit__(self, exc_type, exc_val, exc_tb):
        flag = True
        # 如果代码执行出错，则返回False，抛出异常
        if exc_type is not None:
            flag = False
        self.cx.commit()
        self.cu.close()
        self.cx.close()
        return flag
