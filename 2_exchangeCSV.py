
# coding: utf-8

# In[3]:


# coding: utf-8
import sys
sys.path.append('/users/ytomi/appdata/local/programs/python/python36-32/lib/site-packages')

from xbrl import XBRLParser
import os, re, csv
from collections import defaultdict

default_tag = ['file_nm','element_id','amount']
custom_tag = ['unit_ref','decimals','contextref']
encode_type = 'utf-8'

class XbrlParser(XBRLParser):
    def __init__(self, xbrl_filepath):
        self.xbrl_filepath = xbrl_filepath

    def parse_xbrl(self):
        # parse xbrl file
        with open(self.xbrl_filepath,'r',encoding='utf-8') as of:
            xbrl = XBRLParser.parse(of) # beautiful soup type object
        result_dicts = defaultdict(list)
        _idx = 0

        #print xbrl
        name_space = 'jp*'
        for node in xbrl.find_all(name=re.compile(name_space+':*')):
            if self.ignore_pattern(node):
                continue

            row_dict = defaultdict(list)
            #default tag
            row_dict['file_nm'] = self.xbrl_filepath.rsplit('/', 1)[1]
            row_dict['element_id'] = node.name
            row_dict['amount'] = node.string

            #cutom tag
            for tag in custom_tag:
                row_dict[tag] = self.get_attrib_value(node,tag)

            result_dicts[_idx] = row_dict
            _idx += 1
        return result_dicts

    def ignore_pattern(self, node):
        if 'xsi:nil' in node.attrs:
            if node.attrs['xsi:nil']=='true':
                return True
        #結果が空の場合は対象外にする
        if not isinstance(node.string, str):
            return True
        # 改行コードが結果にある場合対象外にする
        if str(node.string).find(u'\n') > -1:
            return True
        #text文字列は解析に利用できないため、対象外
        if u'textblock' in str(node.name):
            return True
        return False

    def get_attrib_value(self, node, attrib):
        if attrib in node.attrs.keys():
            return node.attrs[attrib]
        else:
            return None

#ディレクトリ配下のファイルのうちis_xbrl_fileがTrueのもののみ取得する
def fild_all_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not is_xbrl_file(root,file):
                continue
            yield os.path.join(root, file)

def is_xbrl_file(root_path,file_name):
    # xbrlファイルでなければ対象外
    if not file_name.endswith('.xbrl'):
        return False
    # AuditDocは対象外
    if u'AuditDoc' in str(root_path):
        return False
    return True

def dump_file(writer,info_dicts):
    _idx = 0
    while _idx < len(info_dicts):
        row_dict = info_dicts[_idx]
        writer.writerow(row_dict)
        _idx += 1

def main():
    base_path = os.getcwd()+'/xbrl_files'

    #writerオブジェクト生成
    resultCsvWriter = csv.DictWriter(
                            open('eggs.csv', 'w',encoding=encode_type)
                        ,   default_tag + custom_tag
                        ,   lineterminator="\n")
    resultCsvWriter.writeheader()

    #対象ファイルを抽出
    xbrl_files = fild_all_files(base_path)
    count = 0
    for xbrl_file in xbrl_files:
        count += 1
        print ('getting data...'+xbrl_file)
        xp = XbrlParser(xbrl_file)
        info_dicts = xp.parse_xbrl()
        dump_file(resultCsvWriter,info_dicts)

if __name__=='__main__':
    main()

