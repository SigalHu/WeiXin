# WeiXin
#### 基于aiohttp的微信公众平台开发

## 介绍
本项目搭建在阿里云平台，反向代理6670端口，目前实现的功能有：**聊天机器人（图灵）、图片识别（face++）、点歌（网易云音乐）、浏览新闻（今日头条）**。
## 准备
* python3.6
* mysql 14.14
* 注册[微信公众平台](https://mp.weixin.qq.com/)
* 注册[图灵机器人](http://www.tuling123.com/)
* 注册[Face++](https://www.faceplusplus.com.cn/)
## 开始之前
由于微信公众平台需要的80端口已经被apache占用，所以需要基于apache配置反向代理。
1. 创建sites-available与sites-enabled目录，sites-available目录将会存放所有的虚拟主机文件，而sites-enabled目录将会存放我们想对外提供服务的主机的符号链接
```shell
mkdir /usr/local/apache/sites-available
mkdir /usr/local/apache/sites-enabled
```
2. 编辑apache的配置文件，
```shell
vi /usr/local/apache/conf/httpd.conf
```
找到以下两条，把#号去掉
```
#LoadModule proxy_module modules/mod_proxy.so
#LoadModule proxy_http_module modules/mod_proxy_http.so
```
在文件末尾添加一行用以声明额外配置文件所在的可选目录
```
IncludeOptional sites-enabled/*.conf
```
3. 在sites-available目录下创建文件
```shell
vi /usr/local/apache/sites-available/web.conf
```
并添加如下内容，当微信服务器访问ServerName的80端口时，将会指向6670端口
```xml
<VirtualHost *:80>
	ServerName 此处填写你在微信公众平台上绑定的域名或IP
	ServerAlias 此处填写你在微信公众平台上绑定的域名或IP
	ProxyPass / http://127.0.0.1:6670/
	ProxyPassReverse / http://127.0.0.1:6670/
</VirtualHost>
```
4. 在sites-enabled目录下创建符号链接，**注意：此处必须使用完整路径**
```shell
ln -s /usr/local/apache/sites-available/web.conf /usr/local/apache/sites-enabled/web.conf
```
5. 重启apache
```shell
service httpd restart
```
#### 参考链接
[http://www.jianshu.com/p/b34c78bf9bf0](http://www.jianshu.com/p/b34c78bf9bf0)</br>
[http://blog.csdn.net/zhouyingge1104/article/details/44459655](http://blog.csdn.net/zhouyingge1104/article/details/44459655)
## 配置文件格式
```xml
<?xml version="1.0" encoding="utf-8"?>
<config>
	<MySQL>
		<user>your_user</user>
		<passwd>your_passwd</passwd>
	</MySQL>
	<微信公众平台>
		<appid>your_appid</appid>
		<secret>your_secret</secret>
	</微信公众平台>
	<图灵机器人>
		<key>your_key</key>
	</图灵机器人>
	<FacePlusPlus>
		<api_key>your_api_key</api_key>
		<api_secret>your_api_secret</api_secret>
	</FacePlusPlus>
</config>
```
## 相关文章
[通过Apache反向代理实现微信服务器80端口访问](http://blog.csdn.net/u011475134/article/details/69951987)</br>
[使用python-aiohttp搭建微信公众平台](http://blog.csdn.net/u011475134/article/details/70147484)</br>
[使用python-aiohttp爬取网易云音乐](http://blog.csdn.net/u011475134/article/details/70183360)</br>
[使用python-aiohttp爬取今日头条](http://blog.csdn.net/u011475134/article/details/70198533)
## 效果图
![image](https://github.com/SigalHu/WeiXin/raw/master/img/1.png) ![image](https://github.com/SigalHu/WeiXin/raw/master/img/2.png) ![image](https://github.com/SigalHu/WeiXin/raw/master/img/3.png) ![image](https://github.com/SigalHu/WeiXin/raw/master/img/4.png) ![image](https://github.com/SigalHu/WeiXin/raw/master/img/5.png) ![image](https://github.com/SigalHu/WeiXin/raw/master/img/6.png)
