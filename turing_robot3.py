import asyncio
# import json
from aiohttp import ClientSession
import random
import myid3

__ARTICLE_NUM = 4
__turingError = (40001,40002,40004,40007)
__turingTitle = {100000:'文本',
				 200000:'链接',
				 302000:'新闻',
				 308000:'菜谱'}

async def __fetch(url,data,loop):
	try:
		async with ClientSession(loop=loop) as session:
			async with session.post(url, data=data,timeout=5) as response:
				# return json.loads(await response.text())
				# print(await response.text())
				return await response.json(content_type='json')
	except Exception as ex:
		print('__fetch:%s' % ex)

async def getTextInfo(text,userid,loop):
	global __turingTitle,__ARTICLE_NUM
	urlTuring = 'http://www.tuling123.com/openapi/api'
	dataTuring = {'key': myid3.get_TuringRobot_key(),
				  'info': text,
				  'userid': userid}

	result = None
	try:
		task = asyncio.ensure_future(__fetch(urlTuring, dataTuring,loop),loop=loop)
		taskDone = await asyncio.wait_for(task,timeout=5)

		if 'code' in taskDone and taskDone['code'] in __turingTitle:
			result = taskDone
			result['title'] = __turingTitle[result['code']]
			del result['code']

			if result['title'] == '新闻' or result['title'] == '菜谱':
				if len(result['list']) > __ARTICLE_NUM:
					result['list'] = random.sample(result['list'], __ARTICLE_NUM)
				result['list'].sort(key=lambda obj: obj.get('icon'), reverse=True)

	except Exception as ex:
		print('getTextInfo:%s' % ex)
	return result

def __main():
	if not myid3.init('config.xml'):
		print('读取配置文件失败！')
		return

	loop = asyncio.get_event_loop()
	text = '新闻'
	task = asyncio.ensure_future(getTextInfo(text,1234,loop),loop=loop)
	taskDone = loop.run_until_complete(task)
	print(taskDone)
	loop.close()

if __name__ == '__main__':
	__main()
