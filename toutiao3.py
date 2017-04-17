import asyncio
from aiohttp import ClientSession
import time
import math
import hashlib

__NEWS_NUM = 8   # hu 返回的最大新闻数
__cookie = None

def getASCP():
	t = int(math.floor(time.time()))
	e = hex(t).upper()[2:]
	m = hashlib.md5()
	m.update(str(t).encode(encoding='utf-8'))
	i = m.hexdigest().upper()

	if len(e) != 8:
		AS = '479BB4B7254C150'
		CP = '7E0AC8874BB0985'
		return AS,CP

	n = i[0:5]
	a = i[-5:]
	s = ''
	r = ''
	for o in range(5):
		s += n[o] + e[o]
		r += e[o + 3] + a[o]

	AS = 'A1' + s + e[-3:]
	CP = e[0:3] + r + 'E1'
	return AS,CP

async def __fetch(url,data,loop):
	global __cookie
	try:
		async with ClientSession(cookies=__cookie,loop=loop) as session:
			# hu 发送GET请求，params为GET请求参数，字典类型
			async with session.get(url, params=data,timeout=5) as response:
				if response.cookies and 'tt_webid' in response.cookies:
					__cookie = {'tt_webid':response.cookies['tt_webid'].value}
				# hu 以json格式读取响应的body并返回字典类型
				return await response.json()
	except Exception as ex:
		print('__fetch:%s' % ex)

async def getNewsInfo(loop):
	global __NEWS_NUM
	AS,CP = getASCP()
	urlTouTiao = 'http://www.toutiao.com'
	urlNews = 'http://www.toutiao.com/api/pc/feed/'
	dataNew = {'category': 'news_hot',
			   'utm_source': 'toutiao',
			   'widen': '1',
			   'max_behot_time': '0',
			   'max_behot_time_tmp':'0',
			   'tadrequire':'true',
			   'as':AS,
			   'cp':CP}
	result = None
	try:
		task = asyncio.ensure_future(__fetch(urlNews, dataNew,loop),loop=loop)
		taskDone = await asyncio.wait_for(task,timeout=5)
		if 'message' not in taskDone or taskDone['message'] != 'success':
			return result

		result = {'max_behot_time':taskDone['next']['max_behot_time'],
				  'news':[]}

		for news_hot in taskDone['data']:
			news = {'Title': None,
					'Description': None,
					'PicUrl': None,
					'Url': None}
			# hu 去掉广告
			if news_hot['is_feed_ad']:
				continue
			news['Title'] = news_hot['title']
			if 'abstract' in news_hot:
				news['Description'] = news_hot['abstract']
			else:
				news['Description'] = ''
			if 'image_url' in news_hot:
				news['PicUrl'] = news_hot['image_url']
			else:
				news['PicUrl'] = ''
			news['Url'] = urlTouTiao + news_hot['source_url']
			result['news'].append(news)
			if len(result['news']) == __NEWS_NUM:
				break
		# hu 把有图片的新闻放到前面
		result['news'].sort(key=lambda obj: obj.get('PicUrl'), reverse=True)
	except Exception as ex:
		print('getNewsInfo:%s' % ex)
	return result

def __main():
	loop = asyncio.get_event_loop()
	for ii in range(2):
		task = asyncio.ensure_future(getNewsInfo(loop),loop=loop)
		taskDone = loop.run_until_complete(task)
		print(__cookie)
		print(taskDone['max_behot_time'])
		for res in taskDone['news']:
			print(res)
	loop.close()

if __name__ == '__main__':
	__main()
