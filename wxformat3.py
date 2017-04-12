class WXFormat:
	@staticmethod
	def text2wx(ToUserName, FromUserName, CreateTime, Content):
		MsgType = 'text'
		result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, Content)
		return result

	@staticmethod
	def netease2wx(resp, ToUserName, FromUserName, CreateTime):
		if resp is None:
			MsgType = 'text'
			Content = '要不换首歌吧，这个真找不到啊'
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, Content)
		else:
			MsgType = 'news'
			MusicCount = len(resp)
			musics = [None] * MusicCount

			for ii, music in zip(range(MusicCount), resp):
				musics[ii] = '''
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
''' % ('%s-%s' % (music['name'],music['artist']), music['artist'], music['picUrl'], music['page'])
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
%s
</Articles>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, MusicCount, ''.join(musics))

		return result

	@staticmethod
	def toutiao2wx(resp, ToUserName, FromUserName, CreateTime):
		if resp is None:
			MsgType = 'text'
			Content = '找不到新闻啦'
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, Content)
		else:
			MsgType = 'news'
			NewsCount = len(resp)
			news = [None] * NewsCount

			for ii, article in zip(range(NewsCount), resp):
				news[ii] = '''
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
''' % (article['Title'], article['Description'], article['PicUrl'], article['Url'])
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
%s
</Articles>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, NewsCount, ''.join(news))

		return result

	@staticmethod
	def turing2wx(resp, ToUserName, FromUserName, CreateTime):
		result = 'success'
		if resp is None:
			return result

		elif resp['title'] == '文本':
			MsgType = 'text'
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, resp['text'])

		elif resp['title'] == '链接':
			MsgType = 'text'
			Content = '%s：<a href="%s">点这里</a>' % (resp['text'], resp['url'])
			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<Content><![CDATA[%s]]></Content>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, Content)

		elif resp['title'] == '新闻':
			MsgType = 'news'
			ArticleCount = len(resp['list'])
			articles = [None] * ArticleCount

			for ii, article in zip(range(ArticleCount), resp['list']):
				articles[ii] = '''
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
''' % (article['article'], article['source'], article['icon'], article['detailurl'])

			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
%s
</Articles>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, ArticleCount, ''.join(articles))

		elif resp['title'] == '菜谱':
			MsgType = 'news'
			ArticleCount = len(resp['list'])
			articles = [None] * ArticleCount

			for ii, article in zip(range(ArticleCount), resp['list']):
				articles[ii] = '''
<item>
<Title><![CDATA[%s]]></Title>
<Description><![CDATA[%s]]></Description>
<PicUrl><![CDATA[%s]]></PicUrl>
<Url><![CDATA[%s]]></Url>
</item>
''' % (article['name'], article['info'], article['icon'], article['detailurl'])

			result = '''<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[%s]]></MsgType>
<ArticleCount>%d</ArticleCount>
<Articles>
%s
/Articles>
</xml>''' % (ToUserName, FromUserName, CreateTime, MsgType, ArticleCount, ''.join(articles))
		return result
