import asyncio
from aiohttp import ClientSession
import random

__MUSIC_NUM = 4

async def __fetch(url,data,loop):
	try:
		async with ClientSession(loop=loop) as session:
			async with session.post(url, data=data,timeout=5) as response:
				return await response.json()
	except Exception as ex:
		print('__fetch:%s' % ex)

async def getMusicInfo(keyword, loop):
	global __MUSIC_NUM
	urlFace = 'http://s.music.163.com/search/get'
	dataMusic = {'type': '1',
				's': keyword,
				'limit': '100',
				'offset': '0'}
	result = None
	try:
		task = asyncio.ensure_future(__fetch(urlFace, dataMusic,loop),loop=loop)
		taskDone = await asyncio.wait_for(task,timeout=5)
		if 'result' not in taskDone:
			return result

		random.shuffle(taskDone['result']['songs'])  # hu 打乱顺序
		for song in taskDone['result']['songs']:
			if result is None:
				result = [{'name':song['name'],
						   'artist':song['artists'][0]['name'],
						   'picUrl':song['album']['picUrl'],
						   'audio':song['audio'],
						   'page':song['page']}]
			else:
				isContained = False
				for rt in result:
					if rt['name'] == song['name'] and rt['artist'] == song['artists'][0]['name']:
						isContained = True
						break
				if isContained:
					continue
				else:
					result.append({'name': song['name'],
								   'artist': song['artists'][0]['name'],
								   'picUrl': song['album']['picUrl'],
								   'audio': song['audio'],
								   'page': song['page']})
					if len(result) == __MUSIC_NUM:
						break

	except Exception as ex:
		print('getMusicInfo:%s' % ex)
	return result

def __main():
	loop = asyncio.get_event_loop()
	music = '彩虹'
	player = '乔楚熙'
	task = asyncio.ensure_future(getMusicInfo(music+player,loop),loop=loop)
	taskDone = loop.run_until_complete(task)
	print(len(taskDone))
	for song in taskDone:
		print(song)
	loop.close()

if __name__ == '__main__':
	__main()
