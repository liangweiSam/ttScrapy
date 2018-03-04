import requests
import sys, io, os
import time, datetime
import random

from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as BFS
from multiprocessing import Process
from selenium import webdriver


'''
	title: h1 class_ = article-title
	content： div class_ = article-content
	p ---- text img
'''
# Class ttDocument(object):

# 	def __init__(self):

# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# desired_capabilities["phantomjs.page.settings.userAgent"] = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'  
# desired_capabilities["phantomjs.page.settings.loadImages"] = False 
# Proxy = webdriver.Proxy()
# Proxy.proxy_type = ProxyType.MANUAL
# Proxy.http_proxy = '123.161.153.5:49969'
# Proxy.add_to_capabilities(desired_capabilities)  
# browser = webdriver.PhantomJS()
# browser.start_session(desired_capabilities)

def getContent(url):
	browser = webdriver.PhantomJS()

	headUrl = r'http://www.toutiao.com/'
	browser.get(headUrl+url)
	
	soup = BFS(browser.page_source, 'lxml')
	title = soup.find('h1', class_ = 'article-title')
	content = soup.find('div', class_ = 'article-content')

	# print(title.string)
	# print(content)
	if 'ArticleFloder' not in os.listdir():
		os.makedirs('ArticleFloder')
	
	if title != None:

		if '%s.txt' %(title.string) not in os.listdir('ArticleFloder'):

			pA = Process(target = getImage, args = (content, title,))
			pI = Process(target = getAticle, args = (content, title))

			pA.start()
			pI.start()

			pA.join()
			pI.join()
			print('抓取<<%s>>完成 %s' %(title.string, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))

	browser.quit()


def getAticle(content, title):
	print('开始抓取<<%s>>文本 %s' %(title.string, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))
	eachP = content.find_all('p')

	if 'ArticleFloder' not in os.listdir():
		os.makedirs('ArticleFloder')
	
	with open(file = 'ArticleFloder/%s.txt' %(title.string), mode = 'a', encoding = 'utf-8') as article:
		for p in eachP:
			if p.find('img') == None:
				article.write(p.get_text())
			article.write('\n')
	# article.close()
	time.sleep(random.randint(2, 4))
	print('完成<<%s>>文本抓取 %s' %(title.string, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))


def getImage(content, title):
	print('开始抓取<<%s>>图片 %s' %(title.string, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))

	i = 0
	imgSet = content.find_all('img')
	if 'imgFloder' not in os.listdir():
		os.makedirs('imgFloder')

	for img in imgSet:
		time.sleep(random.randint(2, 4))
		if 'gif' not in img.get('src'):
			imgByte = requests.get(url = '%s' %img.get('src'))
			with open(file = 'imgFloder/%s%s.jpg' %(title.get_text()[:5].split()[0], i), mode = 'wb') as imgF:
				imgF.write(imgByte.content)	
		else:
			imgByte2 = requests.get(url = 'https:%s' %img.get('src'), filename = 'imgFloder/%s%s.gif' %(title.get_text[:5].split()[0], i))
			with open(file = 'imgFloder/%s%s.gif' %(title.get_text()[:5].split()[0], i), mode = 'wb') as imgF:
				imgF.write(imgByte2.content)

		i+= 1	
	# imgF.close()			
	

	print('完成<<%s>>图片下载 %s' %(title.string, str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))


if __name__ == '__main__':
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk')
	sys.setrecursionlimit(1000000)
	a = ['i6468494812449341966/', 'i6469899596318376461/']
	for i in a:
		time.sleep(random.randint(2, 4))
		getContent(i)

# /item/6454424661580055053/
# /item/6468494812449341966/
# /item/6469899596318376461/