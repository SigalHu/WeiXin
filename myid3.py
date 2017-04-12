from xml.dom.minidom import parse

__myID = {'MySQL':{'user': None,
				   'passwd': None},
		  '微信公众平台':{'appid': None,
						  'secret': None},
		  '图灵机器人':{'key': None},
		  'FacePlusPlus':{'api_key': None,
						  'api_secret': None}}

def init(xmlName):
	global __myID
	try:
		xml = parse(xmlName)
		xmlRoot = xml.documentElement
		for name in __myID:
			xmlInfo = xmlRoot.getElementsByTagName(name)[0]
			for key in __myID[name]:
				__myID[name][key] = xmlInfo.getElementsByTagName(key)[0].childNodes[0].data
	except Exception as ex:
		print(print('init:%s' % ex))
		return False
	return True

def get_MySQL_user():
	global __myID
	return __myID['MySQL']['user']

def get_MySQL_passwd():
	global __myID
	return __myID['MySQL']['passwd']

def get_WeiXin_appid():
	global __myID
	return __myID['微信公众平台']['appid']

def get_WeiXin_secret():
	global __myID
	return __myID['微信公众平台']['secret']

def get_TuringRobot_key():
	global __myID
	return __myID['图灵机器人']['key']

def get_Face_apikey():
	global __myID
	return __myID['FacePlusPlus']['api_key']

def get_Face_secret():
	global __myID
	return __myID['FacePlusPlus']['api_secret']

def __main():
	init('config.xml')
	print(__myID)

if __name__ == '__main__':
	__main()
