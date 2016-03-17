#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import requests
import json
import csv
url = 'http://www.sfbest.com/comments/ajaxPl/'


iids = ['15822', '37198', '14108', '25382', '12055', '138382', '54895', '56947']
refers = ['http://www.sfbest.com/html/products/16/1800015822.html',
    'http://www.sfbest.com/html/products/44/1800043126.html',
    'http://www.sfbest.com/html/products/15/1800014108.html',
    'http://www.sfbest.com/html/products/26/1800025382.html',
    'http://www.sfbest.com/html/products/13/1800012055.html',
    'http://www.sfbest.com/html/products/139/1800138382.html',
    'http://www.sfbest.com/html/products/55/1800054895.html',
    'http://www.sfbest.com/html/products/190/1800189587.html']
urlids = ['015822', '043126', '014108', '025382', '012055', '138382', '054895', '189587']
pagess = [8014, 1491, 3550, 2606, 1064, 1348, 466, 95]
# pagess = [10, 10, 10, 10, 10, 10, 10, 95]


for i in range(8):
    iid = iids[i]
    filename = urlids[i] + '.csv'
    pages = pagess[i]
    headers = {'content-type': 'application/json',
        'Accept':'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate',
        'Accept-Language':'zh-CN,zh;q=0.8,en;q=0.6',
        'Content-Type':'application/x-www-form-urlencoded',
        # 'Referer':'http://www.sfbest.com/html/products/16/1800' + urlids[i] + '.html',
        'Referer': refers[i],
        'X-Requested-With':'XMLHttpRequest'}
    with open(filename, 'w') as csvfile:
        fieldnames = ['author_id', 'timestamp', 'datetime', 'comment_score', 'comment', 'comment_length', 'product_id', 'rank_id', 'rank_name', 'comment_like', 'image_num']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        author_id = ""
        timestamp = 0
        datetime = ""
        comment_score = 0
        comment = ""
        comment_length = 0
        product_id = ""
        rank_id = 0
        rank_name = ""
        comment_like = 0
        image_num = 0

        for page in range(pages):
            print page
            body = 'pid=' + iid + '&page=' + str(page + 1) + '&pageNum=10&type=0'

            r = requests.post(url, data=body, headers=headers)
            js = json.loads(r.content)
            for item in js['data']['data']:
                author_id = item['author_id']
                timestamp = int(item['time'])
                timeArray = time.localtime(timestamp)
                datetime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
                comment_score = int(item['comment_score'])
                comment = item['comment']
                # print comment
                # print type(comment)
                comment_length = len(comment)
                product_id = item['product_id']
                try:
                    rank_id = int(item['rankInfo']['rankId'])
                    rank_name = item['rankInfo']['rankName']
                except:
                    continue
                # print rank_name
                # print type(rank_name)
                comment_like = int(item['comment_like'])
                if item.has_key('images'):
                    image_num = int(len(item['images']))
                else:
                    image_num = 0

                writer.writerow({
                    'author_id': author_id,
                    'timestamp': timestamp,
                    'datetime': datetime,
                    'comment_score': comment_score,
                    'comment': comment,
                    'comment_length': comment_length,
                    'product_id': product_id,
                    'rank_id': rank_id,
                    'rank_name': rank_name,
                    'comment_like': comment_like,
                    'image_num': image_num})
