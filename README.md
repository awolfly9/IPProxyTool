##  开源 & 免费代理工具 IPProxyTool
使用 scrapy 爬虫抓取代理网站，获取大量的免费代理 ip。循环过滤出所有可用的 ip，存入数据库以供其他项目使用<br>
我目前开发的很多爬虫项目都用到了这个代理工具，稳定高效抓取大量数据必备神器。可以访问我的个人站点，查看我的更多有趣项目 [awolfly9](http://awolfly9.com/)

## 项目依赖
* python 2.7.12
* scrapy
* BeautifulSoup
* requests
* pymysql
* web.py
* scrapydo
* lxml
* 安装 mysql 并启动

安装命令：

```
$ pip install Scrapy BeautifulSoup requests pymysql web.py scrapydo lxml
```

## 克隆使用
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
	'charset': 'utf8',
}
```


运行启动脚本 ipproxytool.py。 也可以分别运行抓取，验证，服务器接口脚本，运行方法参考项目说明

```
$ python ipproxytool.py
```

**如果更新后运行报错，请先删除本地数据库。**
<br>


## 项目说明
### 抓取代理网站
所有抓取代理网站的代码都在 [proxy](https://github.com/awolfly9/IPProxyTool/tree/master/ipproxytool/spiders/proxy)<br>
#### 扩展抓取其他的代理网站
	1.在 proxy 目录下新建脚本并继承自 BaseSpider
	2.设置 name、urls、headers
	3.重写 parse_page 方法，提取代理数据
	4.将数据存入数据库 可以参考 ip181.py kuaidaili.py
	5.如果需要抓取特别复杂的代理网站，可以参考 peuland.py
#### 修改 runspider.py 导入抓取库，添加到抓取队列

运行 runspider.py 脚本开始抓取代理网站

```
$ python runspider.py
```

### 验证代理 ip 是否有效
	1.从上一步抓取并存储的数据库中取出所有的代理 IP
	2.利用取出的代理 IP 去请求 http://httpbin.org/get?show_env=1
	3.根据请求结果判断出代理 IP 的有效性，是否支持 HTTPS 以及匿名度，
	  并存储到表 httpbin 中
	4.从 httpbin 表中取出代理去访问目标网站，例如 豆瓣网
	5.如果请求在合适的时间返回成功的数据，则认为这个代理 IP 有效

一个目标网站对应一个脚本，所有验证代理 ip 的代码都在 [validator](https://github.com/awolfly9/IPProxyTool/tree/master/ipproxytool/spiders/validator)

#### 扩展验证其他网站
	1.在 validator 目录下新建脚本并继承 Validator
	2.设置 name、timeout、urls、headers
	3.然后调用 init 方法,可以参考 baidu.py douban.py
	4.如果需要特别复杂的验证方式，可以参考 assetstore.py
#### 修改 runvalidator.py 导入验证库，添加到验证队列
运行 runvalidator.py 脚本验证代理 ip

```
$ python runvalidator.py
```

### 获取代理 ip 数据服务器接口
在 config.py 中修改启动服务器端口配置 data_port，默认为 8000
启动服务器

```
$ python runserver.py
```

## 服务器提供接口
#### 获取
[http://127.0.0.1:8000/select?name=douban&anonymity=1&
https=yes&sort=speed&count=100](http://127.0.0.1:8000/select?name=douban&anonymity=1&https=yes&sort=speed&count=100)

#### 参数

| Name    | Type   | Description   | must |
| ----    | ----   | ----          | ---- |
| name    | str    | 数据库名称      | 是   |
| anonymity | int  | 1:高匿 2:匿名 3:透明 | 否 |
| https     | str  | https:yes http:no  | 否 |
| order     | str  | table 字段  | 否 |
| sort      | str | asc 升序，desc 降序 | 否 |
| count | int | 获取代理数量，默认 100 | 否 |

	
	

#### 删除 
[http://127.0.0.1:8000/delete?name=free_ipproxy&ip=27.197.144.181](http://127.0.0.1:8000/delete?name=free_ipproxy&ip=27.197.144.181)

#### 参数
| Name | Type | Description | 是否必须|
| ----| ---- | ---- | --- |
| name | str | 数据库名称 |  是 |
| ip | str | 需要删除的 ip | 是 |

#### 插入
[http://127.0.0.1:8000/insert?name=douban&ip=555.22.22.55&
port=335&country=china&anonymity=1&
https=yes&speed=5&source=100](http://127.0.0.1:8000/insert?name=douban&ip=555.22.22.55&port=335&country=%E4%B8%AD%E5%9B%BD&anonymity=1&https=yes&speed=5&source=100)

#### 参数
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



## TODO
* 添加抓取更多免费代理网站，目前支持的抓取的免费代理 IP 站点，目前有一些国外的站点连接不稳定
  * (国外) <http://www.freeproxylists.net/>
  * (国外) <http://gatherproxy.com/>
  * (国内) <https://hidemy.name/en/proxy-list/>
  * (国内) <http://www.ip181.com/>
  * (国内) <http://www.kuaidaili.com/>
  * (国外) <https://proxy.peuland.com/proxy_list_by_category.htm>
  * (国外) <https://list.proxylistplus.com/>
  * (国内) <http://m.66ip.cn>
  * (国外) <http://www.us-proxy.org/>
  * (国内) <http://www.xicidaili.com>
* 分布式部署项目
* ~~添加服务器获取接口更多筛选条件~~
* ~~多进程验证代理 IP~~
* ~~添加 https 支持~~
* ~~添加检测 ip 的匿名度~~


## 项目更新
-----------------------------2017-3-30----------------------------<br> 
1.修改完善 readme<br>
2.数据插入支持事务<br>
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


## 参考
* [IPProxyPool](https://github.com/qiyeboy/IPProxyPool)









