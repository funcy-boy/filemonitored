# 使用须知
> 推荐使用python虚拟环境

安装依赖包

```bash
pip install -r requirements.txt
```

1、在`temp\setting.py`中修改数据库连接
 ```json
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.mysql',
		'NAME': 'databasename', #修改数据库名称
		'USER': 'user', #修改用户名
		'HOST': 'host', #数据库地址
		'PASSWORD': 'password', #数据库密码
	}
}
```

2、创建数据库

```bash
create database databasename;
grant all on databasename.* to user@'host' identified by 'password';
```

3、生成数据库表

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

4、运行服务

```bash
python3 manage.py runserver
```
### Docker部署

```bash
docker-compose up -d 
```