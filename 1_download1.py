
# coding: utf-8

# In[20]:


import requests
import json
import os
import io
import shutil
import multiprocessing
from collections import defaultdict
from zipfile import ZipFile

proc = 1    # TODO:マルチプロセス制御（初期値：1並列）

def make_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def download_all_xbrl_files(info_dicts):
    # xbrl_filesのディレクトリが存在しないとき、作成する
    directory_path = os.getcwd()+'/xbrl_files/'
    make_directory(directory_path)
    mp_dict = defaultdict(dict)
    counter = 0

    for _id, info_dict in info_dicts.items():
        #分散処理用にデータを設定
        mp_dict[counter] = info_dict
        counter += 1

    p = 0
    jobs = []
    while(p < proc):
        job = multiprocessing.Process(target=_download_xbrl_file, args=(mp_dict,p,))
        jobs.append(job)
        job.start()
        p += 1

    [job.join() for job in jobs]

#is_yuho関数に当てはまる全ての企業×有報情報IDごとに取得する
def _download_xbrl_file(info_dicts,p):
    no = p
    directory_path = os.getcwd()+'/xbrl_files/'
    while(no < len(info_dicts)):
        info_dict = info_dicts[no]
        no += proc

        # 証券CDごとのディレクトリ作成
        company_path = directory_path + info_dict['cd'] + '/'
        ir_path = company_path + info_dict['id']
        make_directory(company_path)

        #　証券コード×IR情報ごとのディレクトリ作成
        if os.path.exists(ir_path):
            continue
        make_directory(ir_path)
        print('Process('+str(p + 1) + '):downloading:' + info_dict['update']+'_'+info_dict['title'])

        url = info_dict['url']
        r = requests.get(url)
        if r.ok:
            #Requestによりファイルを取得して、Unzipする
            r = requests.get(url)
            z = ZipFile(io.BytesIO(r.content))
            z.extractall(ir_path) # unzip the file and save files to path.

def download_json_url():
    search_directory = os.getcwd()+'/downloaded_info/'
    old_directory = search_directory + 'old/'
    make_directory(old_directory)
    count = 0
    for file_name in os.listdir(search_directory):
        if not u'.json' in file_name :continue
        print(file_name + ' loading...')
        with open(search_directory + file_name,'r') as of:
            info_dict = json.load(of)
        print('downliading:' + str(count) + '~' + str(count+len(info_dict)) )
        count += len(info_dict)

        download_all_xbrl_files(info_dict)
        shutil.move(search_directory + file_name, old_directory + file_name)

if __name__=='__main__':
    download_json_url()


# # coding: utf-8
# import sys
# sys.path.append('/users/ytomi/appdata/local/programs/python/python36-32/lib/site-packages')
# 
# from xbrl import XBRLParser
# import os, re, csv
# from collections import defaultdict
# 
# default_tag = ['file_nm','element_id','amount']
# custom_tag = ['unit_ref','decimals','contextref']
# encode_type = 'utf-8'
# 
# class XbrlParser(XBRLParser):
#     def __init__(self, xbrl_filepath):
#         self.xbrl_filepath = xbrl_filepath
# 
#     def parse_xbrl(self):
#         # parse xbrl file
#         with open(self.xbrl_filepath,'r',encoding='utf-8') as of:
#             xbrl = XBRLParser.parse(of) # beautiful soup type object
#         result_dicts = defaultdict(list)
#         _idx = 0
# 
#         #print xbrl
#         name_space = 'jp*'
#         for node in xbrl.find_all(name=re.compile(name_space+':*')):
#             if self.ignore_pattern(node):
#                 continue
# 
#             row_dict = defaultdict(list)
#             #default tag
#             row_dict['file_nm'] = self.xbrl_filepath.rsplit('\\' or '/', 1)[1]
#             row_dict['element_id'] = node.name
#             row_dict['amount'] = node.string
# 
#             #cutom tag
#             for tag in custom_tag:
#                 row_dict[tag] = self.get_attrib_value(node,tag)
# 
#             result_dicts[_idx] = row_dict
#             _idx += 1
#         return result_dicts
# 
#     def ignore_pattern(self, node):
#         if 'xsi:nil' in node.attrs:
#             if node.attrs['xsi:nil']=='true':
#                 return True
#         #結果が空の場合は対象外にする
#         if not isinstance(node.string, str):
#             return True
#         # 改行コードが結果にある場合対象外にする
#         if str(node.string).find(u'\n') > -1:
#             return True
#         #text文字列は解析に利用できないため、対象外
#         if u'textblock' in str(node.name):
#             return True
#         return False
# 
#     def get_attrib_value(self, node, attrib):
#         if attrib in node.attrs.keys():
#             return node.attrs[attrib]
#         else:
#             return None
# 
# #ディレクトリ配下のファイルのうちis_xbrl_fileがTrueのもののみ取得する
# def fild_all_files(directory):
#     for root, dirs, files in os.walk(directory):
#         for file in files:
#             if not is_xbrl_file(root,file):
#                 continue
#             yield os.path.join(root, file)
# 
# def is_xbrl_file(root_path,file_name):
#     #xbrlファイルでなければ対象外
#     if not file_name.endswith('.xbrl'):
#         return False
#     #AuditDocは対象外
#     if u'AuditDoc' in str(root_path):
#         return False
#     return True
# 
# def dump_file(writer,info_dicts):
#     _idx = 0
#     while _idx < len(info_dicts):
#         row_dict = info_dicts[_idx]
#         writer.writerow(row_dict)
#         _idx += 1
# 
# def main():
#     base_path = os.getcwd()+'/xbrl_files'
# 
#     #writerオブジェクト生成
#     resultCsvWriter = csv.DictWriter(
#                             open('eggs.csv', 'w',encoding=encode_type)
#                         ,   default_tag + custom_tag
#                         ,   lineterminator="\n")
#     resultCsvWriter.writeheader()
# 
#     #対象ファイルを抽出
#     xbrl_files = fild_all_files(base_path)
#     count = 0
#     for xbrl_file in xbrl_files:
#         count += 1
#         print ('getting data...'+xbrl_file)
#         xp = XbrlParser(xbrl_file)
#         info_dicts = xp.parse_xbrl()
#         dump_file(resultCsvWriter,info_dicts)
# 
# if __name__=='__main__':
#     main()
