import time
import re
import os
import random
import multiprocessing as mp
from bs4 import BeautifulSoup
import requests


#file_obj = open("thousand_pages.txt", 'a', encoding='utf-8')

urls = ['https://www.gushiwen.org/shiwen/default.aspx?page='+str(i) for i in range(1, 1001)]
count = 0

AGENT_LIST = [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
]

headers = {
	'authority': 'yijiuningyib.gushiwen.org',
	'method': 'GET',
	'scheme': 'https',
	'accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
	'accept-encoding': 'gzip, deflate, br',
	'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
	'user-agent': random.choice(AGENT_LIST),
	'upgrade-insecure-requests': '1',
}

def parse(url):
	session_used = requests.Session()
	html = session_used.get(url,headers=headers)
	soup = BeautifulSoup(html.content, 'html.parser')
	contents = soup.select('div[class="left"]')[1]
	contents = list(contents.select('div[class="sons"]'))
	poem_datas = []
	rex=re.compile(r'\(.*?\)')
	for c in contents:
		writer = c.select('p[class="source"]')[0].text.replace('：', '::')
		poem = c.select('div[class="contson"]')[0].text.replace('　', '')
		#print(len(c.select('div[class="tag"]')))
		if len(c.select('div[class="tag"]'))!=0:
			poem_label_list = c.select('div[class="tag"]')[0].text.replace('，','')
			poem_label = poem_label_list.replace('\n','|')
		else:
			poem_label = '||'
		poem = re.sub(rex, "", poem)
		poem_datas.append(str(writer.replace('\n', '')+'::'+poem.replace('\n', '')+'::'+ poem_label + '\n'))
	return poem_datas

def html_to_txt(output_data_path):
	with open(output_data_path,'w',encoding='utf-8') as output_data:
		for i in range(1000):
			#print(i)
			try:
				page_data = parse(urls[i])
				for a_poem in page_data:
					output_data.write(a_poem)
			except IOError:
				print("%s the page cannot down"%i)

file_obj = "thousand_pages.txt"

html_to_txt(file_obj)
#print(urls[52])
#print(parse(urls[51]))


