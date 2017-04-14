import pymysql
import datetime
import myid3

class WXSQL:
	__db = None

	def __init__(self):
		try:
			self.__db = pymysql.connect(host='localhost',
										user=myid3.get_MySQL_user(),
										passwd=myid3.get_MySQL_passwd(),
										charset='utf8')
			cursor = self.__db.cursor()
			cursor.execute('create database if not exists weixin')
			cursor.execute('use weixin')
			cursor.execute('''create table if not exists userconfig(
							id char(30) not null primary key,
							menu bool,
							config char(5),
							lasttime datetime,
							neteasemusic_keyword char(20),
							neteasemusic_offset smallint)''')
		except Exception as ex:
			print('MySQL:初始化数据库失败！')

	def __del__(self):
		if self.__db:
			self.__db.close()

	def __getCursor(self):  # hu 防止MySQL8小时后自动断连
		try:
			self.__db.ping(False)
			return self.__db.cursor()
		except Exception as ex:
			self.__db.close()
			self.__db = pymysql.connect(host='localhost',
										user=myid3.get_MySQL_user(),
										passwd=myid3.get_MySQL_passwd(),
										db='weixin',
										charset='utf8')
			print('MySQL:MySQL重新连接！')
			return self.__db.cursor()

	def write(self,ID,menu,config):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select true from userconfig where id = '%s' ''' % ID)
			if cursor.fetchone():
				cursor.execute('''update userconfig set menu=%d,config='%s' 
										where id='%s' ''' % (menu, config,ID))
			else:
				cursor.execute('''insert into userconfig(id,menu,config)
										values('%s',%d,'%s') ''' % (ID,menu,config))
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:修改用户参数失败！')
			return False
		return True

	def read(self,ID):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select menu,config,lasttime from userconfig where id = '%s' ''' % ID)
			results = cursor.fetchall()
			if len(results) == 1:
				return results[0]
		except Exception as ex:
			print('MySQL:读取用户参数失败！')
		return None,None,None

	def writeMenu(self,ID,menu):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select true from userconfig where id = '%s' ''' % ID)
			if cursor.fetchone():
				cursor.execute('''update userconfig set menu=%d 
										where id='%s' ''' % (menu,ID))
			else:
				cursor.execute('''insert into userconfig(id,menu)
										values('%s',%d) ''' % (ID,menu))
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:修改用户参数失败！')
			return False
		return True

	def readMenu(self,ID):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select menu,lasttime from userconfig where id = '%s' ''' % ID)
			results = cursor.fetchall()
			if len(results) == 1:
				nowtime = datetime.datetime.now()
				menu, lasttime = results[0]
				if (nowtime-lasttime) < datetime.timedelta(minutes=1):   # hu 用户设置在1分钟内有效
					return menu
				else:
					self.writeMenu(ID,False)
					return False
		except Exception as ex:
			print('MySQL:读取用户参数失败！')
		return None

	def writeConfig(self,ID,config):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select true from userconfig where id = '%s' ''' % ID)
			if cursor.fetchone():
				cursor.execute('''update userconfig set config='%s' 
										where id='%s' ''' % (config,ID))
			else:
				cursor.execute('''insert into userconfig(id,config)
										values('%s','%s') ''' % (ID,config))
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:修改用户参数失败！')
			return False
		return True

	def readConfig(self,ID):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select config,lasttime from userconfig where id = '%s' ''' % ID)
			results = cursor.fetchall()
			if len(results) == 1:
				nowtime = datetime.datetime.now()
				config, lasttime = results[0]
				if (nowtime-lasttime) < datetime.timedelta(minutes=30):   # hu 用户设置在30分钟内有效
					return config
				else:
					self.delete(ID)
		except Exception as ex:
			print('MySQL:读取用户参数失败！')
		return None

	def writeNeteaseMusic(self, ID, neteasemusic_keyword, neteasemusic_offset=0):
		try:
			cursor = self.__getCursor()
			cursor.execute('''SELECT CHARACTER_MAXIMUM_LENGTH FROM information_schema.COLUMNS 
							  where TABLE_NAME='userconfig' and COLUMN_NAME='neteasemusic_keyword' ''')
			keywordlen = cursor.fetchone()[0]
			if len(neteasemusic_keyword) > keywordlen:
				neteasemusic_keyword = neteasemusic_keyword[:keywordlen]
			cursor.execute('''select true from userconfig where id = '%s' ''' % ID)
			if cursor.fetchone():
				cursor.execute('''update userconfig set neteasemusic_keyword='%s',neteasemusic_offset=%d 
								  where id='%s' ''' % (neteasemusic_keyword, neteasemusic_offset, ID))
			else:
				cursor.execute('''insert into userconfig(id,neteasemusic_keyword,neteasemusic_offset)
								  values('%s','%s',%d) ''' % (ID, neteasemusic_keyword, neteasemusic_offset))
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:修改用户参数失败！')
			return False
		return True

	def readNeteaseMusic(self,ID):
		try:
			cursor = self.__getCursor()
			cursor.execute('''select neteasemusic_keyword,neteasemusic_offset,lasttime from userconfig where id = '%s' ''' % ID)
			results = cursor.fetchall()
			if len(results) == 1:
				nowtime = datetime.datetime.now()
				neteasemusic_keyword, neteasemusic_offset, lasttime = results[0]
				if (nowtime-lasttime) < datetime.timedelta(minutes=30):   # hu 用户设置在30分钟内有效
					cursor.execute('''SELECT CHARACTER_MAXIMUM_LENGTH FROM information_schema.COLUMNS 
									  where TABLE_NAME='userconfig' and COLUMN_NAME='neteasemusic_keyword' ''')
					keywordlen = cursor.fetchone()[0]
					return neteasemusic_keyword,neteasemusic_offset,keywordlen
				else:
					self.delete(ID)
		except Exception as ex:
			print('MySQL:读取用户参数失败！')
		return None,None,None

	def writeLastTime(self,ID):
		try:
			lasttime = datetime.datetime.now()

			cursor = self.__getCursor()
			cursor.execute('''select true from userconfig where id = '%s' ''' % ID)
			if cursor.fetchone():
				cursor.execute('''update userconfig set lasttime='%s' 
										where id='%s' ''' % (lasttime,ID))
			else:
				cursor.execute('''insert into userconfig(id,lasttime)
										values('%s','%s') ''' % (ID,lasttime))
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:修改用户参数失败！')
			return False
		return True

	def delete(self,ID):
		try:
			cursor = self.__getCursor()
			cursor.execute('''delete from userconfig where id = '%s' ''' % ID)
			self.__db.commit()
		except Exception as ex:
			self.__db.rollback()
			print('MySQL:删除用户失败！')
			return False
		return True

def __main():
	if not myid3.init('config.xml'):
		print('读取配置文件失败！')
		return

	sql = WXSQL()
	sql.writeLastTime('12324')
	sql.write('12324',False,'wqww')
	menu, config, lasttime = sql.read('12324')
	print(menu, config, lasttime)

	sql.writeMenu('12324', True)
	menu = sql.readMenu('12324')
	print(menu)

	sql.writeConfig('12324','ggga')
	config = sql.readConfig('12324')
	print(config)

	neteasemusic_keyword, neteasemusic_offset,neteasemusic_keywordlen = sql.readNeteaseMusic('12324')
	print(neteasemusic_keyword,neteasemusic_offset,neteasemusic_keywordlen)
	sql.writeNeteaseMusic('12324','彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹彩虹')
	neteasemusic_keyword, neteasemusic_offset,neteasemusic_keywordlen = sql.readNeteaseMusic('12324')
	print(neteasemusic_keyword,neteasemusic_offset,neteasemusic_keywordlen)

if __name__ == '__main__':
	__main()




