# -*- coding:utf-8 -*-
import requests
import base64
from zlib import crc32
import random
import math
import json


def getVideo(videoUrl):
	headers = {
				'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3376.400 QQBrowser/9.6.11924.400'
				}
	response = requests.get(url = videoUrl,	headers = headers)
	with open('1.mp4', 'wb') as video :
		video.write(response.content)

def getJSUrl(videoId):
	r = str(random.random())[2:]
	finalPath = '/video/urls/v/1/toutiao/mp4/%s?r=%s' %(videoId, r)
	s = crc32(bytes(finalPath, 'utf-8'))
	s = s >> 0
	tt = 'tt_playerbyjyo'
	return 'http://ib.365yg.com' + finalPath + '&s=' + str(s) + '&callback=' + tt 


def getVideoUrl(jsUrl):
	headers = {
				'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3376.400 QQBrowser/9.6.11924.400'
				}
	response = requests.get(url = jsUrl, headers = headers)
	data = json.loads(response.text[15:-1])

	print(base64.decodestring(bytes(data['data']['video_list']['video_1']['main_url'], 'utf-8')))

if __name__ == '__main__':
	jsurl = getJSUrl('f55aebee8d354a6287059ffb9e9dcd8c')
	getVideoUrl(jsurl)

