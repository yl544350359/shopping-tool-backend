# 日本购物工具箱-后端(shopping-tool backend)
本仓库包含了网站[购物工具箱](agonize.asuscomm.com:8000)的后端代码.
This Repo includes codes of the backend of [Shopping-tool](agonize.asuscomm.com:8000).
## v1.1.0 API概要 API Brief Introduction
| 名称/Name | HTTP方法/Method | 路径/Path | data | parameter|
| ----| -------- | ---- | ---- | -------- |
| itemDetail | POST | /itemDetail | {"item_url": ""} | NA |
| getRate | GET | /getRate | NA | NA |

***
## 本地测试 Local test
准备好[实时汇率API](https://fixer.io/documentation)的key.在根目录下新建文件`config.json`,并将你获得的key填入该文件.<br>Please prepare the key for [rate API](https://fixer.io/documentation) before creating `config.json` file under root path. Put your key into that file.
```
{
    "fixer": {
        "key": "Your key"
    }
}
```
安装依赖项<br>Install dependencies
```
pip install -r requirements.txt
```
修改`gunicorn.conf.py`中`bind`参数, 其中`5555`可以替换成其他任何闲置端口.<br>Modify `bind` in `gunicorn.conf.py`. Here, you can `5555` to any other idle port.
```
bind = "127.0.0.1:5555"
```
运行下面命令,即可启动后端.<br> Execute the below command, then you can start the backend.
```
gunicorn wsgi:app
```

***
## 容器化部署 Containernized Deployment
打包docker image<br>Build docker image
```
docker build -t <image name>:<tag> .
```
例如<br>For example
```
docker build -t shopping-tool-backend:v1.0.0 .
```
修改`docker-compose.yml`中的`image`<br>Modify `image` in `docker-compose.yml`
```
web:
    image: <image name>:<tag>
    command: gunicorn wsgi:app -c ./gunicorn.conf.py
    volumes:
      - .:/app
    ports:
      - "8001:8001"
```
例如<br>For example
 ```
 web:
    image: shopping-tool:v1.1.0
    command: gunicorn wsgi:app -c ./gunicorn.conf.py
    volumes:
      - .:/app
    ports:
      - "8001:8001"
 ```
执行如下命令,即可启动后端<br>Execute the below command, then you can start the backend.
```
docker-compose up
```