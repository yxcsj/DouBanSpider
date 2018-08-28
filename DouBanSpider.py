#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import urllib
import requests
from bs4 import BeautifulSoup as bs
import random
import pandas as pd
import re
from operator import itemgetter

def tag_spider():
    '''
    爬取豆瓣图书的所有标签
    '''
    url_tag = 'https://book.douban.com/tag/?icn=index-nav'
    headers_tag = {'User-Agent': 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)'}
    tags = []

    try:
        html_tag = requests.get(url_tag, headers=headers_tag).text
        soup_tag = bs(html_tag,'lxml')
        list_tag = soup_tag.find('div', id = 'wrapper').find_all('a', href =re.compile(r'/tag/'))


        for i in list_tag[1:]:
           tag = i.get_text()
           tags.append(tag)

    except Exception as err:
        print(err)

    return tags


def link_spider(tag):
    '''
    根据标签爬取图书链接，由于此页面的作者、出版社、定价等信息混在一起，所以在图书链接页面在解析数据
    设置随机休眠时间和随机headers信息，有效避免爬虫被封
    '''
    page = 0
    links = []
    key = urllib.parse.quote(tag)
    ua_list =["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",]
    ua = random.choice(ua_list)

    while True:
        url_book = 'https://book.douban.com/tag/' + key + '?start='+ str(page * 20) + '&type=T'
        headers_book = {
            'Accept': r"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8" ,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': r'll="118264"; bid=-0ADuvbTVtg; _vwo_uuid_v2=DF2A25A624BD634A236549FB68EFE1260|d48bf97d1db2a8d358a90597a5699c28; gr_user_id=56c34a7b-95c4-4fa6-8d71-c9e61b5eeb18; __yadk_uid=28xTzlqdrnEkW8QjNGlDR3pXsvGe6Flx; ue="774368030@qq.com"; __utmv=30149280.2592; viewed="1084336_3988517_5407267_26425261_5948760"; douban-fav-remind=1; ps=y; dbcl2="25922351:9UGpCp07H4o"; push_doumail_num=0; __utmz=30149280.1534862378.24.19.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; push_noty_num=0; ck=dQpk; ap_v=1,6.0; __utma=30149280.1145868426.1518767930.1534862378.1534900646.25; __utmc=30149280; gr_cs1_7d6f3f93-8ccc-4568-a290-eb7cdf2b10be=user_id%3A1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1534900663%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=81379588.1886099754.1523265577.1534865271.1534900663.8; __utmc=81379588; __utmz=81379588.1534900663.8.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_id.100001.3ac3=6d83895b974cb485.1523265577.8.1534901984.1534868391.; __utmb=30149280.37.10.1534900646; __utmb=81379588.33.10.1534900663',
            'Host': 'book.douban.com',
            'Referer': r'https://book.douban.com/tag/?icn=index-nav',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': ua,
            }

        sleep(random.uniform(0, 2))  #随机时间休息
        html_book = requests.get(url_book,headers = headers_book).text
        print(u'正在爬取标签 %s 的第 %d 页' %(tag, page))
        page += 1

        #如果出现'没有找到符合条件的图书'表示已经到最后一页，退出循环
        if html_book.find(u'没有找到符合条件的图书') > 0:
            print('标签 %s 的图书,在第%d 已经翻完' % (tag, page))
            break

        soup_book = bs(html_book, 'lxml')
        list_book = soup_book.find('ul', class_=re.compile('subject-list')).find_all('div', class_='info')

        # 解析内容
        for info in list_book:
            try:
                link = info.a['href'].strip()  # 书名
                links.append(link)

            except Exception as e:
                print (e)

    return links


def book_spier(links):
    '''
    根据图书链接，爬取图书信息，并清洗数据，然后存到DataFrame表单中
    设置随机休眠时间和随机headers信息，有效避免爬虫被封
    '''
    books = []
    ua_list =["Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",]

    for link in links:
        try:
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Cache-Control': 'max-age=0',
                'Connection': 'keep-alive',
                'Cookie': 'll="118264"; bid=-0ADuvbTVtg; _vwo_uuid_v2=DF2A25A624BD634A236549FB68EFE1260|d48bf97d1db2a8d358a90597a5699c28; gr_user_id=56c34a7b-95c4-4fa6-8d71-c9e61b5eeb18; __yadk_uid=28xTzlqdrnEkW8QjNGlDR3pXsvGe6Flx; ue="774368030@qq.com"; __utmv=30149280.2592; douban-fav-remind=1; ps=y; dbcl2="25922351:9UGpCp07H4o"; push_doumail_num=0; __utmz=30149280.1534862378.24.19.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/login; push_noty_num=0; __utmz=81379588.1534900663.8.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ct=y; ap_v=1,6.0; __utmc=30149280; __utmc=81379588; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1535352382%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1145868426.1518767930.1535346900.1535352382.44; __utma=81379588.1886099754.1523265577.1535346900.1535352382.27; viewed="26698660_25862578_26889236_1255625_1770782_26893260_26382433_1003000_26701959_2339264"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=d2680b9d-3c78-46a3-a374-4261b8773ee0; gr_cs1_d2680b9d-3c78-46a3-a374-4261b8773ee0=user_id%3A0; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_d2680b9d-3c78-46a3-a374-4261b8773ee0=true; _pk_id.100001.3ac3=6d83895b974cb485.1523265577.27.1535353084.1535347723.; __utmt_douban=1; __utmb=30149280.7.10.1535352382; __utmt=1; __utmb=81379588.7.10.1535352382',
                'Host': 'book.douban.com',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': random.choice(ua_list),
            }
            sleep(random.uniform(1, 2))  # 随机时间休息
            html = requests.get(link, headers = headers).text

            #书名
            pat1 = r'v:itemreviewed">(.*?)</span>'
            title = re.findall(pat1, html)[0].strip()
            #作者
            pat2 = '作者.?<.span>.*?href.*?>(.*?)</a>'
            author = re.findall(pat2, html, re.S)[0]
            author = re.sub(r'\s+', '', author)
            #出版社
            if html.find(u'出版社:') > 0:
                pat3 = '出版社:<.span>(.*?)<br.>'
                press = re.findall(pat3, html, re.S)[0].strip()
            else:
                press = '无'
            #出版年
            if html.find(u'出版年:') > 0:
                pat4 = '出版年:<.span>(.*?)<br.>'
                published = re.findall(pat4, html, re.S)[0].strip()
            else:
                published = '无'
            #译者
            if len(re.findall('译者.?<.span>', html, re.S)) > 0:
                pat5 = '译者.?<.span>.*?href.*?>(.*?)</a>'
                translator = re.findall(pat5, html, re.S)[0].strip()
            else:
                translator = '无'
            #定价
            if html.find(u'定价:') > 0:
                pat6 = '定价:<.span>(.*?)<br.>'
                pricing = re.findall(pat6, html, re.S)[0].strip()
            else:
                pricing = '无'
            if html.find(u'评价人数不足') < 0:
                #评分
                pat7 = 'property="v:average">(.*?)</strong>'
                score = re.findall(pat7, html, re.S)[0].strip()
                # 评论数
                pat8 = '"v:votes">(.*?)</span>人评价'
                num = int(re.findall(pat8, html, re.S)[0].strip())
            else:
                score = 0.0
                num = 0

        except Exception as err:
            print(err)

        books.append((title, score, num, author, press, published, pricing, translator))
        books = list(set(books))

    books = sorted(books, key=itemgetter(1, 2), reverse=True)  #首先按照评分，其次按照评论数，降序排序
    #保存为DataFrame表单
    df_book = pd.DataFrame(data= books, columns=['title', 'score', 'num', 'author', 'press', 'published', 'pricing', 'translator'])
    df_book.rename(columns = {
                        'title':'书名',
                        'score':'评分',
                        'num':'评论数',
                        'author':'作者',
                        'press':'出版社',
                        'published':'出版时间',
                        'pricing':'定价',
                        'translator':'译者'
                    }, inplace= True)

    return df_book


def pipelines(tags):
    '''
    将所有图书数据存到一个excel中，并且每个标签分别存到一个sheet中；
    '''
    writer = pd.ExcelWriter('doubanbook.xlsx')

    for i in range(len(tags)):
        tag = tags[i]
        print(tag)
        links = link_spider(tags[i])
        df_book = book_spier(links)
        df_book.to_excel(writer, sheet_name=tag, index=False)  #将不同的标签的内容，存到不同的sheet中，并以标签名命名sheet
    writer.save()


if __name__ == '__main__':
    tags = tag_spider()
    pipelines(tags)

