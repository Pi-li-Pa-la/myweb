# ! /usr/bin/python
# -*- coding: utf-8 -*-

import time
import struct
import os

# from openpyxl import Workbook, load_workbook
from jinja2 import Environment, FileSystemLoader

log_config = {
}


def set_log_path():
    # 日志函数辅助函数
    fmt = '%Y%m%d%H%M%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    log_config['file'] = 'logs/log.{}.txt'.format(dt)


def log(*args, **kwargs):
    # 日志函数，直接调用即可输出日志
    fmt = '%Y/%m/%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)
    path = log_config.get('file')
    if path is None:
        set_log_path()
        path = log_config['file']
    with open(path, 'a') as f:
        print(dt, *args, file=f, **kwargs)


path = '{}/templates/'.format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


# # 文件类型设置字典
# # 用16进制字符串的目的是可以知道文件头是多少字节
# # 各种文件头的长度不一样，少则2字符，长则8字符
# def type_list():
#     return {
#         # "FFD8FF": "JPEG",
#         # "89504E47": "PNG",
#         "D0CF11E0": "xls",
#         "504B0304": "xlsx",
#     }
#
#
# # 字节码转16进制字符串
# def bytes2hex(bytes):
#     num = len(bytes)
#     hex_str = u""
#     for i in range(num):
#         t = u"%x" % bytes[i]
#         if len(t) % 2:
#             hex_str += u"0"
#         hex_str += t
#     return hex_str.upper()
#
#
# # 获取文件类型，读取其二进制文件并根据文件头的数据判断其文件类型
# def file_type(filename):
#     binfile = open(filename, 'rb')  # 必需二制字读取
#     tl = type_list()
#     ftype = False
#     for hcode in tl.keys():
#         num_of_bytes = int(len(hcode) / 2)  # 需要读多少字节
#         binfile.seek(0)  # 每次读取都要回到文件头，不然会一直往后读取
#         hbytes = struct.unpack_from("B" * num_of_bytes, binfile.read(num_of_bytes))  # 一个 "B"表示一个字节
#         f_hcode = bytes2hex(hbytes)
#         if f_hcode == hcode:
#             ftype = True
#             break
#     binfile.close()
#     return ftype
#
#
# # openpyxl复制粘贴某区域(由cells组成的tuple)
# # openpyxl自身未实现复制一片单元格的功能，此函数为补充此功能
# def copy_range(source_range, target_range):
#     l = len(source_range)
#     for n in range(l):
#         target_range[n].value = source_range[n].value
#
#
# def trans_col(column):
#     # openpyxl中若直接获取单元格的列则会返回大写字母，此函数将其翻译为数字
#     trans_dict = {
#         'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9, 'J': 10, 'K': 11, 'L': 12, 'M': 13,
#         'N': 14, 'O': 15, 'P': 16, 'Q': 17, 'R': 18, 'S': 19, 'T': 20, 'U': 21, 'V': 22, 'W': 23, 'X': 24, 'Y': 25,
#         'Z': 26,
#     }
#     columns = column[::-1]
#     col_num = 0
#     n = 0
#     for c in columns:
#         col_num += trans_dict[c] * (26 ** n)
#         n += 1
#     return col_num
#
#
# def del_row(wb, sht, *delete_row):
#     """
#     由于openpyxl中未实现删除行这个功能，此函数补充此功能。
#     删除行的实现：新建另一个新的workbook，然后复制要删除行的workbook的其他sheet
#     当复制到被删除行的sheet时，逐行复制数据。
#     当复制到被删除的行时，跳过此行继续复制
#     """
#     new_wb = Workbook()
#     new_wb.active.title = wb[wb.sheetnames[0]].title
#     for name in wb.sheetnames:
#         if name != wb[wb.sheetnames[0]].title:
#             new_wb.create_sheet(name)
#     for sheet in wb:
#         rows = sheet.rows
#         n = 0
#         for r in rows:
#             if (r[0].row in delete_row) and (sheet.title == sht.title):
#                 n += 1
#             else:
#                 for cell in r:
#                     new_wb[sheet.title].cell(row=cell.row - n, column=trans_col(cell.column)).value = cell.value
#     return new_wb

