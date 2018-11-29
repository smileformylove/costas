#coding=utf-8
#spider_wallpaper.py
import requests
import os
import time
from bs4 import BeautifulSoup 

refer = 'http://desk.zol.com.cn'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0'}  #给请求指定一个请求头来模拟chrome浏览器
headers_cf = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:63.0) Gecko/20100101 Firefox/63.0',
				'Referer': refer,
				}
web_url = 'http://desk.zol.com.cn/fengjing/c7/'

def download(web_url):
	r = requests.get(web_url, headers=headers) #像目标url地址发送get请求，返回一个response对象
	page_tot = BeautifulSoup(r.content, 'html.parser').find_all('a', class_='pic')
	for index, item in enumerate(page_tot[0:-4]):
		title = item.select('span')[0].get('title')
		num = item.select('span')[0].text[-4:-2]
		if num < "10":
			num = item.select('span')[0].text[-3:-2]
		num = eval(num)

		folder_path = './picture/' + title
		if os.path.exists(folder_path) == False:
			os.makedirs(folder_path)

		rr = requests.get(refer + item.get('href'))
		rr_all = BeautifulSoup(rr.content, 'html.parser').find_all('a')
		xx = 0
		for item_t in rr_all:
			img = item_t.select('img')
			#print(img)
			if(img):
				height = img[0].get('height')
				width = img[0].get('width')
				if(height == "90" and width == "144"):
					ru = img[0].get('srcs')
					if(ru == None):
						ru = img[0].get('src')
					#print(ru)
					r_url = requests.get(ru)
					xx = xx+1
					path = folder_path + '/' + str(xx) + '.jpg'
					with open(path, 'wb') as f:
						f.write(r_url.content)
						f.close()


		print(xx)
		print('The %d dataset has downloaded!' % (index+1))

download(web_url)
download(web_url + '2.html')