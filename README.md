# zxSchool

单独开启
 python manage.py runserver 8000 --insecure
 最终开启
 1. 开启uwsgi  
uwsgi -i /root/ZxOnline/conf/uwsgi/uwsgi.ini
2. 开启nginx
sudo systemctl restart nginx


# 服务器端
## python3.7安装


1. 安装依赖包  
    yum install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel gcc gcc-c++  openssl-devel libffi-devel python-devel mariadb-devel

    
2. 下载python源码 
```shell script
    wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz  
    tar -xzvf Python-3.7.3.tgz -C  /tmp  
    cd  /tmp/Python-3.7.3/ 
``` 
 

3. 把Python3.7安装到 /usr/local 目录  
    ./configure --prefix=/usr/local
    make  
    make altinstall   #这一步比较耗时  

6. 更改/usr/bin/python链接  
    ln -s /usr/local/bin/python3.7 /usr/bin/python3  
    ln -s /usr/local/bin/pip3.7 /usr/bin/pip3  

## maridb 和 redis安装
1. 安装  
    sudo yum install mariadb-server
2. 启动， 重启  
    sudo systemctl start mariadb  
    sudo systemctl restart mariadb  
    设置安全规则 配置mysql的端口  
3. 设置bind-ip  
    vim /etc/my.cnf  
    在 [mysqld]:  
        下面加一行  
        bind-address = 0.0.0.0  
4. 设置外部ip可以访问  
    先进入mysql才能运行下面命令:  
        mysql 直接进入就行  
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;  
    GRANT ALL PRIVILEGES ON *.* TO 'root'@'localhost' IDENTIFIED BY '123456' WITH GRANT OPTION;  
    
    FLUSH PRIVILEGES;  
    
5. 设置阿里云的对外端口  
    阿里云为了安全关闭了大多数端口，我们使用快速打开打开需要的端口，没用的手动添加
   

6. 安装mysqlclient出问题

    centos 7：
        yum install python-devel mariadb-devel -y
        # 顺着来的可以跳过，因为已经安装
    ubuntu：
        sudo apt-get install libmysqlclient-dev
        
    然后：
        pip install mysqlclient
        
7. 安装redis
    
    yum install redis
    service redis start
    
    ps aux|grep redis  #查看redis是否启动

##  安装nginx
文档https://www.digitalocean.com/community/tutorials/how-to-install-nginx-on-centos-7  
1. sudo yum install epel-release
2. sudo yum install nginx
3. sudo systemctl start nginx  
sudo systemctl restart nginx

## 安装virtualenvwrapper
```shell script
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3  
yum install python-setuptools python-devel  
pip install virtualenvwrapper  
```

编辑.bashrc  
vim ~/.bashrc  
```shell script
export WORKON_HOME=$HOME/.virtualenvs
source /usr/bin/virtualenvwrapper.sh

source ~/.bashrc
```
找不到文件尝试
```shell script
# 文件位置是否正确
 sudo find / -name virtualenvwrapper.sh
# 若文件位置正确可能是下载了python2版
sudo pip3 install virtualenv virtualenvwrapper

# 创建虚拟环境
mkvirtualenv -p python3 zxonline
workon  # 打开
deactive # 关闭
```
pycharm可以直接使用deployment关联
123.57.131.56:8000

## 安装uwsgi
pip install uwsgi
uwsgi --http :8000 --module MxOnline.wsgi