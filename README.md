## 在系统中安装docker就可以使用本程序：

下载本程序
```
git clone ipproxy
```

然后进入目录：
```
cd ipproxy
```

创建镜像：
```
docker build -t proxy .
```

运行容器：
```
docker run -it proxy
```

## 在config.py中按照自己的需求修改配置信息
```
database_config = {
    'host': 'localhost',
    'port': 3306,
    'user': 'root',
    'password': 'root',
    'charset': 'utf8',
}
```