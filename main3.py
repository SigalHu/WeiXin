import asyncio
from aiohttp import web
from aiohttp import ClientSession
import re
import face3
import turing_robot3
from mysql3 import WXSQL
from wxformat3 import WXFormat
import netease_music3
import toutiao3
import myid3

__wxSQL = None
__wxMenu = {'1': '自言自语',
			'2': '图片识别',
			'3': '在线点歌',
			'4': '今日头条'}

def __getWXMenu():
	global __wxMenu
	strMenu = '回复序号：\n'
	for key,value in __wxMenu.items():
		strMenu += '%s. %s\n' % (key,value)
	return strMenu[:-1]

async def __postClient(url,data,body,loop):
	try:
		async with ClientSession(loop=loop) as session:
			async with session.post(url, params=data,data=body,timeout=5) as response:
				# print(response.url)
				return await response.json()
	except Exception as ex:
		print('__postClient:%s' % ex)

async def __getClient(url,data,loop):
	try:
		async with ClientSession(loop=loop) as session:
			async with session.get(url, params=data,timeout=5) as response:
				return await response.json()
	except Exception as ex:
		print('__getClient:%s' % ex)

def __initwxmenu(loop):
	urlToken = 'https://api.weixin.qq.com/cgi-bin/token'
	dataToken = {'grant_type':'client_credential',
				'appid':myid3.get_WeiXin_appid(),
				'secret':myid3.get_WeiXin_secret()}
	urlMenu = 'https://api.weixin.qq.com/cgi-bin/menu/create'
	dataMenu = {'access_token':None}
	bodyNenu = {'button':[{'name':'功能'},{'name','帮助'}]}
	try:
		task = asyncio.ensure_future(__getClient(urlToken, dataToken,loop),loop=loop)
		taskDone = loop.run_until_complete(asyncio.wait_for(task,timeout=5))
		dataMenu['access_token'] = taskDone['access_token']
		task = asyncio.ensure_future(__postClient(urlMenu, dataMenu,bodyNenu,loop),loop=loop)
		taskDone = loop.run_until_complete(asyncio.wait_for(task,timeout=5))
		print(taskDone)
	except Exception as ex:
		print('__initwxmenu:%s' % ex)

async def getIndex(request):
	# urls = {'场景图片':'https://ss0.bdstatic.com/94oJfD_bAAcT8t7mm9GUKT-xh_/timg?image&quality=100&size=b4000_4000&sec=1490149870&di=d0c10abe5fb9eed5644ad52bbc964a49&src=http://img1.3lian.com/2015/a1/91/d/48.jpg',
	# 		'人脸图片':'https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1490199785816&di=9a2f2c8de645690753a244be9c8c95e8&imgtype=0&src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fw%253D580%2Fsign%3D54903c5d720e0cf3a0f74ef33a47f23d%2Ffb2bd688d43f87946000d961d21b0ef41ad53a74.jpg'}
	#
	# picInfo = await face3.getPicInfo(urls['场景图片'], request.app.loop)
	# print(picInfo)
	# picInfo = await face3.getPicInfo(urls['人脸图片'], request.app.loop)
	# print(picInfo)
	return web.Response(body='hello JuJu!\nby Sigal'.encode('utf-8'))

async def getWX(request):
	# print(request.query)
	echostr = 'success'
	try:
		reg = 'echostr=(.*?)&'
		echostr = re.findall(reg, request.query_string)[0]
	except Exception as ex:
		pass
	return web.Response(body=echostr.encode('utf-8'))

async def postWX(request):
	global __wxSQL
	info = await request.text()
	reg = r'''<xml><ToUserName><!\[CDATA\[(.*?)\]\]></ToUserName>
<FromUserName><!\[CDATA\[(.*?)\]\]></FromUserName>
<CreateTime>(.*?)</CreateTime>
<MsgType><!\[CDATA\[(.*?)\]\]></MsgType>'''
	ToUserName, FromUserName, CreateTime, MsgType = re.findall(reg, info)[0]

	result = 'success'
	Content = None

	if MsgType.lower() == 'text':
		reg = r'''<Content><!\[CDATA\[(.*?)\]\]></Content>
<MsgId>(.*?)</MsgId>'''
		Content, MsgId = re.findall(reg, info)[0]
	elif MsgType.lower() == 'voice':
		reg = r'''<MediaId><!\[CDATA\[(.*?)\]\]></MediaId>
<Format><!\[CDATA\[(.*?)\]\]></Format>
<MsgId>(.*?)</MsgId>
<Recognition><!\[CDATA\[(.*?)\]\]></Recognition>'''
		MediaId, Format, MsgId, Content = re.findall(reg, info)[0]
	elif MsgType.lower() == 'event':   	# hu 用户订阅或取消订阅
		reg = r'''<Event><!\[CDATA\[(.*?)\]\]></Event>'''
		Event = re.findall(reg, info)[0]
		if Event.lower() == 'subscribe':
			Content = '回复菜单，给你看看我的超能力'
			result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)
		elif Event.lower() == 'unsubscribe':
			__wxSQL.delete(FromUserName)
		return web.Response(body=result.encode('utf-8'))

	if __wxSQL.readMenu(FromUserName):   # hu 菜单选择
		# hu 确认用户选择
		if Content in __wxMenu:
			__wxSQL.write(FromUserName, False, __wxMenu[Content])
			if __wxMenu[Content] == '自言自语':
				Content = '好了，我们来聊天吧'
			elif __wxMenu[Content] == '图片识别':
				Content = '快把你的图片给我看看'
			elif __wxMenu[Content] == '在线点歌':
				Content = '来，悄悄告诉我你想听的歌'
			elif __wxMenu[Content] == '今日头条':
				Content = '回复任意内容就可以看到新闻了哦'
		else:
			Content = __getWXMenu()
		result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)

	else:
		userConfig = __wxSQL.readConfig(FromUserName)

		if Content == '菜单':
			__wxSQL.writeMenu(FromUserName,True)
			Content = __getWXMenu()
			result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)

		elif userConfig == '图片识别':
			if MsgType.lower() == 'image'.lower():
				reg = r'''<PicUrl><!\[CDATA\[(.*?)\]\]></PicUrl>
<MsgId>(.*?)</MsgId>
<MediaId><!\[CDATA\[(.*?)\]\]></MediaId>'''
				PicUrl, MsgId, MediaId = re.findall(reg, info)[0]
				Content = await face3.getPicInfo(PicUrl, request.app.loop)
			else:
				Content = '骗人，这不是图片啊啊啊'
			result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)

		elif userConfig == '在线点歌':
			if MsgType.lower() == 'text' or MsgType.lower() == 'voice':
				resp = await netease_music3.getMusicInfo(Content, request.app.loop)
				result = WXFormat.netease2wx(resp, FromUserName, ToUserName, CreateTime)
			else:
				Content = '你当我傻啊，这不是歌名吧'
				result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)

		elif userConfig == '今日头条':
			resp = await toutiao3.getNewsInfo(request.app.loop)
			result = WXFormat.toutiao2wx(resp['news'], FromUserName, ToUserName, CreateTime)

		else:   # hu 默认为自言自语
			if MsgType.lower() == 'text' or MsgType.lower() == 'voice':
				resp = await turing_robot3.getTextInfo(Content, FromUserName, request.app.loop)
				result = WXFormat.turing2wx(resp, FromUserName, ToUserName, CreateTime)
			else:
				Content = '这个我不会呢，聊些别的吧，要不输入菜单试试看？也许会有惊喜哦'
				result = WXFormat.text2wx(FromUserName, ToUserName, CreateTime, Content)

	__wxSQL.writeLastTime(FromUserName)  # hu 更新用户最近一次访问时间
	return web.Response(body=result.encode('utf-8'))

def __main():
	global __wxSQL

	if not myid3.init('config.xml'):
		print('读取配置文件失败！')
		return

	loop = asyncio.get_event_loop()
	# __initwxmenu(loop)
	__wxSQL = WXSQL()
	app = web.Application(loop=loop)
	app.router.add_route('GET', '/', getIndex)
	app.router.add_route('GET', '/WeiXin', getWX)
	app.router.add_route('POST', '/WeiXin', postWX)
	web.run_app(app, port=6670)
	loop.close()

if __name__ == '__main__':
	__main()
