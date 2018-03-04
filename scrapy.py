# -*- coding:utf-8 -*-
import requests as RS 
import urllib.request as request
from selenium import webdriver
from bs4 import BeautifulSoup as BFS 
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.proxy import ProxyType
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from  selenium.webdriver.support.ui import WebDriverWait
import sys, io, os, re
import time
import ttDocument
import random

'''
	www.toutiao.com
	根据科技版面的发布者的名字进行抓取
	抓取距离当天日期大于5天， 且阅读量大于3W， 或评论数大于20
	抓十篇
'''

'''
	每个头条号账号内部的链接
	a class_ = lbtn source

	文章的链接
	a class_ = link title
		

	页面内全部文章
	div class_ = y-left
	阅读量--可以直接进去文章内部
	a class_ = lbtn
	评论量
	a class_ = lbtn comment
	日期
	span class_ = lbtn
'''
# desired_capabilities = DesiredCapabilities.PHANTOMJS.copy()
# desired_capabilities["phantomjs.page.settings.userAgent"] = r'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3408.400 QQBrowser/9.6.12028.400'  
# desired_capabilities["phantomjs.page.settings.loadImages"] = False 
# Proxy = webdriver.Proxy()
# Proxy.proxy_type = ProxyType.MANUAL
# Proxy.http_proxy = '123.161.153.5:49969'
# Proxy.add_to_capabilities(desired_capabilities)  
# browser.start_session(desired_capabilities)

def getContent(target):
	browser = webdriver.PhantomJS()
	url = r'http://www.toutiao.com'
	language = r'/ch/'
	i = 0
	# browser = webdriver.PhantomJS()
	print('程序开始运行....')
	browser.get(url+language+target)
	time.sleep(3) 

	soup = BFS(browser.page_source, 'lxml')
	authorSet = soup.find_all('a', class_ = 'lbtn source')
	# authorSet.append('https://www.toutiao.com/c/user/6092443523/')

	getAuthorPage('http://www.toutiao.com/c/user/6092443523/', browser)		
	time.sleep(5)

	for author in authorSet:
		if author != None:
			print('执行获取作者集')
		if 'search' not in author.get('href'):
			if i > 10:
				break
			getAuthorPage(url+author.get('href'), browser)		
			time.sleep(5)			
			i+=1
	browser.quit()
	# except Exception as e:
	# print('获取数据失败！%s'  %(e))
		
def getAuthorPage(url, browser):
	
	browser.get(url)
	#需要给时间来获取网页
	time.sleep(random.randint(2, 5))
	
	page = BFS(browser.page_source, 'lxml')
	href = ''
	items = page.find_all('div', class_ = 'y-left')
	
	print(url)
	print('获取文章集')
	for itemA in items:
			pageView = itemA.find('a' , 'lbtn')
			# 获得阅读量
			if pageView == None:
				print('空页面')
				continue
			else:
				amount = pageView.string[:-4]
				if '万' not in amount:
					continue
				else:
					amount = amount[:-1]
					
					if float(amount) >= 1:
						href = pageView.get('href')
					else:
						comment = itemA.find('a', 'lbtn comment')
						# 获得评论量
						if comment != None:
							comAmount = comment.string.strip()[:-2]
						if int(comAmount) > 5:
							href = pageView.get('href')	
						else:
							print('沒有符合條件的文章')
			ttDocument.getContent('i'+href[6:])
			print('%s' %(amount))
			time.sleep(1)



if __name__ == '__main__':
	sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='gbk')
	sys.setrecursionlimit(1000000)
	target = 'news_tech/'
	target2 = 'nba/'
	target3 = 'football_italy/'
	target4 = 'news_entertainment/'
	target5 = 'csl/'
	getContent(target3)
	print('程序完成！')