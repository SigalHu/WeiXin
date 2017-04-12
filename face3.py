import asyncio
from aiohttp import ClientSession
import myid3

async def __fetch(url,data,loop):
	try:
		async with ClientSession(loop=loop) as session:
			async with session.post(url, data=data,timeout=5) as response:
				return await response.json()
	except Exception as ex:
		print('__fetch:%s' % ex)

async def getPicInfo(image_url,loop):
	urlFace = 'https://api-cn.faceplusplus.com/facepp/v3/detect'
	dataFace = {'api_key': myid3.get_Face_apikey(),
				'api_secret': myid3.get_Face_secret(),
				'image_url': image_url,
				'return_landmark': '0',
				'return_attributes': 'gender,age,smiling,ethnicity'}

	urlScene = 'https://api-cn.faceplusplus.com/imagepp/beta/detectsceneandobject'
	dataScene = {'api_key': myid3.get_Face_apikey(),
				'api_secret': myid3.get_Face_secret(),
				'image_url': image_url}

	result = '场景：None\n物品：None'

	try:
		tasks = [asyncio.ensure_future(__fetch(urlFace, dataFace,loop),loop=loop),
				asyncio.ensure_future(__fetch(urlScene, dataScene,loop),loop=loop)]
		tasksDone, tasksPending = await asyncio.wait(tasks)

		for taskDone in tasksDone:
			info = taskDone.result()
			if 'faces' in info:
				if not info['faces']:
					continue
				gender = info['faces'][0]['attributes']['gender']['value']
				age = info['faces'][0]['attributes']['age']['value']
				ethnicity = info['faces'][0]['attributes']['ethnicity']['value']
				smile = info['faces'][0]['attributes']['smile']['value']
				result = '性别：%s\n年级：%s\n人种：%s\n微笑指数：%s' % (gender, age, ethnicity, smile)
				break
			elif 'scenes' in info:
				if info['scenes']:
					scenes = info['scenes'][0]['value']
				else:
					scenes = 'None'
				if info['objects']:
					objects = info['objects'][0]['value']
				else:
					objects = 'None'
				result = '场景：%s\n物品：%s' % (scenes, objects)
	except Exception as ex:
		print('getPicInfo:%s' % ex)
	return result

def __main():
	if not myid3.init('config.xml'):
		print('读取配置文件失败！')
		return

	loop = asyncio.get_event_loop()
	urls = {'场景图片':'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1490149870&di=d0c10abe5fb9eed5644ad52bbc964a49&src=http://img1.3lian.com/2015/a1/91/d/48.jpg',
			'人脸图片':'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1490199785816&di=9a2f2c8de645690753a244be9c8c95e8&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fw%253D580%2Fsign%3D54903c5d720e0cf3a0f74ef33a47f23d%2Ffb2bd688d43f87946000d961d21b0ef41ad53a74.jpg'}
	tasks = [asyncio.ensure_future(getPicInfo(urls['场景图片'],loop),loop=loop),
			 asyncio.ensure_future(getPicInfo(urls['人脸图片'],loop),loop=loop)]
	tasksDone,tasksPending = loop.run_until_complete(asyncio.wait(tasks))
	for taskDone in tasksDone:
		print(taskDone.result())
	loop.close()

if __name__ == '__main__':
	__main()
