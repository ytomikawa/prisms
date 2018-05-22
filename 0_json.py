
# coding: utf-8

# In[3]:


import requests
import xml.etree.ElementTree as ET
import json
import os
import io
import re
import multiprocessing
from collections import defaultdict
from datetime import datetime as dt

proc = 1    # TODO:マルチプロセス制御（初期値：1並列）

def get_link_info_str(ticker_symbol, base_url):
    url = base_url+ticker_symbol
    response = requests.get(url)
    return response.text

def get_link(tree, namespace, since):
    yuho_dict = defaultdict(dict)
    #entryタグ毎にforeach
    for el in tree.findall('.//'+namespace+'entry'):

        #titleタグに有価証券の文字があれば、後続処理を実行
        title = el.find(namespace+'title').text
        if not is_yuho(title): continue

        updated = el.find(namespace+'updated').text
        if not time_check(updated,since): return yuho_dict

        # zipファイルのアドレスを辞書オブジェクトへ登録
        _id = el.find(namespace+'id').text
        link = el.find('./'+namespace+'link[@type="application/zip"]')
        url = link.attrib['href']
        cd = re.sub(r'^【(\w+)】.*',r"\1",title)
        yuho_dict[_id] = {'id':_id,'title':title,'cd':cd,'url':url,'update':updated}
    return yuho_dict

def is_yuho(title):
    if u'有価証券報告書' in str(title):
        return True
    else:
        return False

def time_check(update,since):
    updated_time = dt.strptime(update, '%Y-%m-%dT%H:%M:%S+09:00')
    return updated_time>=since

def make_directory(dir_name):
    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

def write_download_info(ofname,info_dict):
    with open(ofname,'w') as of:
        json.dump(info_dict, of, indent=4)

def multi_controller(since):
    p = 0
    jobs = []
    while(p < proc):
        job = multiprocessing.Process(target=craete_xbrl_url_json, args=(since,p,))
        jobs.append(job)
        job.start()
        p += 1
    [job.join() for job in jobs]

def craete_xbrl_url_json(since,p):
    #有報キャッチャーWebServiceのAtomAPIアドレス<http://resource.ufocatch.com/>
    base_url = 'http://resource.ufocatch.com/atom/edinetx/query/'
    namespace = '{http://www.w3.org/2005/Atom}'
    #有報キャッチャーのページ
    page = 1 + p
    count = 0

    while True:
        #文字列変換
        t_symbol = str(page)
        print('page:'+t_symbol + ', loading...')

        #企業毎の有報へのデータへのリンク情報を取得
        response_string = get_link_info_str(t_symbol, base_url)
        

        #すでに取得したファイルかどうかをチェックする
        path = './downloaded_info/dat_download_'+t_symbol+'.json'
        if os.path.exists(path) == True :
            page += 1
            continue
        
        #xmlをparseするElementTreeを取得
        ET_tree = ET.fromstring( response_string )
        ET.register_namespace('',namespace[1:-1])
        

        #downloadファイルの対象を取得
        info_dict = get_link(ET_tree,namespace,since)
        count += len(info_dict)
        if len(info_dict) == 0 : 
            #取得データがなくなり次第、処理終了
            print('process' + str(p) + ':complete a download!! [' + str(count) + ']')
            break

        #Request用のJson形式のファイルを作成
        json_directory=os.getcwd()+'/downloaded_info'
        make_directory(json_directory)
        ofname = json_directory+'/dat_download_'+t_symbol+'.json'
        write_download_info(ofname,info_dict)

        page += proc

if __name__=='__main__':
    #TODO 取得データの末尾（以下例では、2015/07/17以降のデータを取得）
    since = dt.strptime('2015-04-11','%Y-%m-%d')
    print('since:', since)
    #一定期間に発生したデータ全てのURLを取得する
    multi_controller(since)

