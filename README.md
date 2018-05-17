## 项目运行说明
### 运行环境配置
1. 在`pyenv`或`virtualenv`中新建`python`环境并激活；
2. 在激活的环境中使用`pip`安装项目使用的第三方库。

如果是Windows请先在环境中安装已经编译好的pycrypto和mysql-python二进制包。
```
easy_install pycrypto-xxx.exe
easy_install MySQL-python-xxx.exe
```

```
pip install -r requirements/common.txt
```

### 数据库配置

#### 1. 新建数据库
```
create database ask_price_db;
```

#### 2. 导入数据库文件
```
mysql -uroot -p123456 ask_price_db < ask_price_db.sql   # mysql -u用户名 -p密码 数据库名 < 数据库名.sql
```

#### 3. 并在项目的`settings`目录下新建`my_dev.cnf`文件，文件内容为

```
[client]
database = 数据库名
user = 数据库用户名
password = 数据库密码
port = 数据库端口（一般为3306）
host = localhost
default-character-set = utf8
```