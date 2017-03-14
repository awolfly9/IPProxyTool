# IPProxyTool
使用 scrapy 爬虫抓取代理网站，获取大量的免费代理 ip。过滤出所有可用的 ip，存入数据库以备使用。

####个人项目欢迎加微信吐槽
![](weixin.png)

##运行环境
python 2.7.12

###运行依赖包
* scrapy   
* BeautifulSoup
* requests
* mysql-connector-python [安装参考](http://stackoverflow.com/questions/31748278/how-do-you-install-mysql-connector-python-development-version-through-pip) 
* web.py
* scrapydo
* lxml



###安装 Mysql

* 安装 Mysql 并启动
* 安装 mysql-connector-python [安装参考](http://stackoverflow.com/questions/31748278/how-do-you-install-mysql-connector-python-development-version-through-pip)


##下载使用
将项目克隆到本地

```
$ git clone https://github.com/awolfly9/IPProxyTool.git
```

进入工程目录

```
$ cd IPProxyTool
```
修改 mysql 数据库配置 [config.py](https://github.com/awolfly9/IPProxyTool/blob/master/config.py) 中 database_config 的用户名和密码为数据库的用户名和密码

```
$ vim config.py
---------------

database_config = {
	'host': 'localhost',
	'port': 3306,
	'user': 'root',
	'password': '123456',
}
```


运行启动脚本 ipproxytool.py 也可以分别运行抓取，验证，服务器接口脚本，运行方法参考项目说明

```
$ python ipproxytool.py
```


##项目说明
####抓取代理网站
所有抓取代理网站的代码都在 [proxy](https://github.com/awolfly9/IPProxyTool/tree/master/ipproxytool/spiders/proxy)<br/>
#####扩展抓取其他的代理网站
1.在 proxy 目录下新建脚本并继承自 BaseSpider <br/>
2.设置 name、urls、headers<br/>
3.重写 parse_page 方法，提取代理数据<br/>
4.将数据存入数据库 具体可以参考 [ip181](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/proxy/ip181.py)                 [kuaidaili](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/proxy/kuaidaili.py)<br/>
5.如果需要抓取特别复杂的代理网站，可以参考[peuland](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/proxy/peuland.py)<br/>

#####修改 runspider.py 导入抓取库，添加到抓取队列

可以单独运行 runspider.py 脚本开始抓取代理网站

```
$ python runspider.py
```

####验证代理 ip 是否有效
目前验证方式：<br>
1.从上一步抓取并存储的数据库中取出所有的代理 IP <br>
2.利用取出的代理 IP 去请求 [httpbin](http://httpbin.org/get?show_env=1)<br>
3.根据请求结果判断出代理 IP 的有效性，是否支持 HTTPS 以及匿名度，并存储到表 httpbin 中<br>
4.从 httpbin 表中取出代理去访问目标网站，例如 [豆瓣](https://www.douban.com/)<br>
5.如果请求在合适的时间返回成功的数据，则认为这个代理 IP 有效。并且存入相应的表中<br>

一个目标网站对应一个脚本，所有验证代理 ip 的代码都在 [validator](https://github.com/awolfly9/IPProxyTool/tree/master/ipproxytool/spiders/validator)
#####扩展验证其他网站
1.在 validator 目录下新建脚本并继承 Validator <br>
2.设置 name、timeout、urls、headers <br>
3.然后调用 init 方法,可以参考 [baidu](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/validator/baidu.py) [douban](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/validator/douban.py)<br>
4.如果需要特别复杂的验证方式，可以参考 [assetstore](https://github.com/awolfly9/IPProxyTool/blob/master/ipproxytool/spiders/validator/assetstore.py)<br>
#####修改runvalidator.py 导入验证库，添加到验证队列
可以单独运行 runvalidator.py 开始验证代理ip的有效性

```
$ python runvalidator.py
```

###获取代理 ip 数据服务器接口
在 config.py 中修改启动服务器端口配置 data_port，默认为 8000
启动服务器

```
$ python runserver.py
```

服务器提供接口
####获取
<http://127.0.0.1:8000/select?name=httpbin&anonymity=1&https=yes&order=id&sort=desc&count=100>

参数

| Name    | Type   | Description   | must |
| ----    | ----   | ----          | ---- |
| name    | str    | 数据库名称      | 是   |
| anonymity | int  | 1:高匿 2:匿名 3:透明 | 否 |
| https     | str  | https:yes http:no  | 否 |
| order     | str  | table 字段  | 否 |
| sort      | str | asc 升序，desc 降序 | 否 |
| count | int | 获取代理数量，默认 100 | 否 |

	
	

####删除 
<http://127.0.0.1:8000/delete?name=httpbin&ip=27.197.144.181>

参数

| Name | Type | Description | 是否必须|
| ----| ---- | ---- | --- |
| name | str | 数据库名称 |  是 |
| ip | str | 需要删除的 ip | 是 |

####插入
<http://127.0.0.1:8000/insert?name=httpbin&ip=555.22.22.55&port=335&country=%E4%B8%AD%E5%9B%BD&anonymity=1&https=yes&speed=5&source=100>

参数

| Name | Type | Description | 是否必须|
| ----| ---- | ---- | ----|
| name | str | 数据库名称 |是 |
| ip | str | ip 地址 | 是|
| port | str | 端口 |是|
| country | str | 国家 |否|
| anonymity | int | 1:高匿,2:匿名,3:透明  |否|
| https | str | yes:https,no:http |否|
| speed | float | 访问速度 |否|
| source | str | ip 来源 |否|


##TODO
* 添加抓取更多免费代理网站
* 分布式部署项目
* ~~添加服务器获取接口更多筛选条件~~
* ~~添加 https 支持~~
* ~~添加检测 ip 的匿名度~~


##参考
* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)


##项目更新
-----------------------------2017-3-14----------------------------<br> 
1.更改服务器接口，添加排序方式<br>
2.添加多进程方式验证代理 ip 的有效性<br>
<br>
-----------------------------2017-2-20----------------------------<br> 
1.添加服务器获取接口更多筛选条件<br>
<br>

-----------------------------2017-2-16----------------------------<br> 
1.验证代理 IP 的匿名度<br>
2.验证代理 IP HTTPS 支持<br>
3.添加 httpbin 验证并发数设置，默认为 4











