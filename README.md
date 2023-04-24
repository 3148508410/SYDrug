## SYDrug
Django-Pharmaceutical sales mall
心如潭水静无风邀请您进行远程控制
ToDesk设备代码:261 157 441（该用户已设置禁止临时密码连接）

## 一、项目搭建
#### 1.创建项目及app
**·**创建项目：

python manage.py startproject SYDrug
**·** 创建app：

python manage.py startapp user # 用户模块
python manage.py startapp goods # 商品模块
python manage.py startapp carts # 购物车模块
python manage.py startapp order # 订单模块
#### 2.数据库配置及文件
**·** 需要手动创建数据库： 

    create database SYDrug charset=utf8;
**·** settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'SYDrug',
            'USER': 'root',
            'PASSWORD': 'root',
            'host': '127.0.0.1',
            'PORT': 3306,
        } 
    
    # 服务器上
    # 1. 创建远程访问MySQL的用户名和密码：
    CREATE USER 'chenglong'@'%' IDENTIFIED BY '123456';
    # 2.授予远程访问MySQL用户特定的数据库权限：
    GRANT ALL PRIVILEGES ON SYDrug.* TO 'chenglong'@'%';
    # 3.将更改保存到MySQL配置文件d中：
    FLUSH PRIVILEGES;
    # 4.修改MySQL配置文件以允许远程访问：
        # 打开MySQL配置文件“/etc/mysql/mysql.conf.d/mysqld.cnf”，找到以下行：
        bind-address = 127.0.0.1
        # 将其更改为：
        bind-address = 0.0.0.0
    # 5.重新启动MySQL服务器：
    sudo service mysql restart

    # 6.查看mysql账号信息
    cat /etc/passwd | grep 'chenglong'
    # 7.开放服务器端口3306
    sudo ufw allow 3306
    sudo ufw allow 3306/tcp

    # 8.root身份导出数据库数据
    mysqldump -u root -p --databases SYDrug > sydrug.sql

    # 9.导入数据
    mysql -u chenglong -p sydrug < sydrug.sql

    导入数据失败，报错：没有权限修改数据库，则以root身份进入数据库，然后：
    #在 MySQL 终端中，使用以下命令为用户创建帐户和授权：
    CREATE USER 'username'@'localhost' IDENTIFIED BY 'password';
    GRANT ALL PRIVILEGES ON SYDrug.* TO 'username'@'localhost';
    # 立即生效
    FLUSH PRIVILEGES;

#### 3.语言及时区配置
**·** settings.py

    LANGUAGE_CODE = 'zh-hans'
    TIME_ZONE = 'Asia/Shanghai'
    
#### 4.静态文件配置
**·** manage.py同级目录创建static文件夹，settings.py做如下配置
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
#### 5.urls配置
**·** SYDrug/urls
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('user/', include('apps.user.urls', namespace='user'),),  # 用户模块
        path('cart/', include('apps.cart.urls', namespace='cart')),  # 购物车模块
        path('order/', include('apps.order.urls', namespace='goods')),  # 订单模块
        path('', include('apps.goods.urls', namespace='order')),  # 商品模块（首页）

    ]
**·** 其它四个应用的urls复制
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [

    ]
#### 6.数据库继承
    # 创建数据库类继承modeles.Model, 新增三个字段  db/base_model.py
    from django.db import models


    class BaseModel(models.Model):
        """ 模型抽象基类 """
        create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
        update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
        is_delete = models.BooleanField(default=False, verbose_name='删除标记')

        class Meta:
            # 说明是一个抽象类
            abstract = True

    # settings.py 添加下面内容， 不加此处迁移时会出错

    # django认证系统使用的模型类
    AUTH_USER_MODEL='user.User'
#### 7.富文本编辑器的安装
**·** 安装
    pip install django-tinymce
**·** 注册
**·** settings.py添加配置项
    # 富文本编辑器的配置
    TINYMCE_DEFAULT_CONFIG = {
        'theme': 'advanced',
        'width': 600,
        'height': 400,
    }
## 注册功能的实现
**1** 加入静态网页模板
**2** user.views显示
    from django.shortcuts import render


    # Create your views here.
    # /user/register
    def register(request):
        """ 显示注册页面 """
        return render(request, 'register.html')
**3** user.urls中进行配置
    from django.contrib import admin
    from django.urls import path, include
    from . import views

    urlpatterns = [
        path('register/', views.register, name="register"),  # 注册

    ]
**4** 编辑templates的register.html
    # 加载静态文件
    ......
    {% load static %}
    <head>
            <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">
            <title>天天生鲜-注册</title>
            <link rel="stylesheet" type="text/css" href="{% static 'css/reset.css' %}">
        <link rel="stylesheet" type="text/css" href="{% static 'css/main.css' %}">
    ......

    # form表单的设置
            <form method="post" action="/user/register_handle">
        {% csrf_token %}
                
**5** 类视图的使用
**·** /user/views.py
    class RegisterView(View):
        """ 注册 """

        def get(self, request):
            """ 请求方式为get时 """
            pass

        def post(self, request):
            """ 请求方式为post时 """
            pass

    # /user/urls(用as_views方法)
    urlpatterns = [
        path('register/', RegisterView.as_view(), name='register'),  # 注册
        url(r'^active/(?P<tokens>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
        url(r'^login$', LoginView.as_view(), name='login'),  # 登录
    ]
**6** 注册过程进行数据校验
                
**·** 接收数据
                
    username = request.POST.get('user_name')
    password = request.POST.get('pwd')
    confirm_password = request.POST.get('cpwd')
    email = request.POST.get('email')
    allow = request.POST.get('allow')
                
**·** 进行数据校验
                
    if not all([username, password, email]):
    # 数据不完整
        return render(request, 'register.html', {'errmsg': '数据不完整！'})
    # 校验密码
    if password != confirm_password:
        return render(request, 'register.html', {'errmsg': '两次密码输入不一致'})
    # 校验邮箱
    if not re.match(r'^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱格式不正确！'})

    # 校验用户协议
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请勾选用户协议！'})

    # 注册前检查用户名是否已经存在      
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        # 用户名不存在
        user = None
    if user:
        # 用户名已存在
        return render(request, 'register.html', {'errmsg': '用户名已存在'})
        
**7** 注册过程中的业务处理
                
    # /user/views.py
    # 进行业务处理、用户注册
            user = User.objects.create_user(username, password, email)
            user.is_active = 0  # 将用户状态改为0，默认为1（激活状态）
            user.save()

            # 发送激活邮件，http://127.0.0.1:8000/user/active/3
            # 加密用户身份信息，生成激活token
            header = {'alg': 'HS256'}  # 签名算法
            key = settings.SECRET_KEY  # 用于签名的密钥
            info = {'id': user.id}  # 待签名的数据负载
            token = jwt.encode(header=header, payload=info, key=key)  # 生成用户激活token
            token = token.decode()  # 使用utf-8解码

            # 发邮件
            subject = '拾忆医药欢迎您！'
            message = ''
            receiver = [email]
            html_message = '<h1>%s, 欢迎您成为天天生鲜注册会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
                username, token, token)
            send_mail(subject, message, settings.EMAIL_FROM, receiver, html_message=html_message)

            # 返回应答，跳转到首页
            return redirect(reverse('goods:index'))
    
    
**·** settings.py中实现
                
    # 邮件发送的配置
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend' # 指定邮件后端
    EMAIL_HOST = 'smtp.qq.com'
    EMAIL_PORT = 25  # 端口号固定为25
    EMAIL_HOST_USER = '3148508410@qq.com'  # 发件人
    EMAIL_HOST_PASSWORD = 'xfvhkcdpedyodedf'  # qq邮箱授权码
    EMAIL_USE_TLS = False
    EMAIL_FROM = '拾忆医药<3148508410@qq.com>'  # 收件人看到的发件人
**8** 用户激活、登录类视图的实现
    # /user/views 
    class ActiveView(View):
        """用户激活"""

        def get(self, request, token):
            """进行用户激活"""
            # 进行解密，获取要激活的用户信息
            key = settings.SECRET_KEY
            try:
                data = jwt.decode(token, key)
                # 获取用户id
                user_id = data['id']
                user = User.objects.get(id=user_id)
                user.is_active = 1
                user.save()

                # 跳转到登录页面
                return redirect(reverse('user:login'))
            except JoseError:
                return HttpResponse("激活链接失效！")


    class LoginView(View):
        """ 登录 """

        def get(self, request):
            return render(request, 'login.html')
**9** url的配置
    # /user/urls

    from django.conf.urls import url
    from django.contrib import admin
    from django.urls import path, include
    from . import views
    from .views import RegisterView, ActiveView, LoginView

    urlpatterns = [
        # path('register/', views.register, name="register"),  # 注册
        # path('register_handle/', views.register_handle, name="register_handle")  # 注册处理
        path('register/', RegisterView.as_view(), name='register'),  # 注册
        url(r'^active/(?P<token>.*)$', ActiveView.as_view(), name='active'),  # 用户激活
        url(r'^login$', LoginView.as_view(), name='login'),  # 登录
    ]
**10** 用户激活生成token
                
     # 加密用户身份信息，生成激活token
            header = {'alg': 'HS256'}  # 签名算法
            key = settings.SECRET_KEY  # 用于签名的密钥
            info = {'id': user.id}  # 待签名的数据负载
            token = jwt.encode(header=header, payload=info, key=key)  # 生成用户激活token
            token = token.decode()  # 使用utf-8解码
     # 解密token还原数据
        def get(self, request, token):
            """进行用户激活"""
            # 进行解密，获取要激活的用户信息
            key = settings.SECRET_KEY
            try:
                data = jwt.decode(token, key)
                # 获取用户id
                user_id = data['id']
                user = User.objects.get(id=user_id)
                user.is_active = 1
                user.save()
                
**11** 注册交给Celery进行处理
**·** celery_tasks/tasks.py
    # 使用celery
    from django.core.mail import send_mail
    from django.conf import settings
    from celery import Celery
    import time

    # 在任务处理者一端加这几句
    # import os
    # import django
    # os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SYDrug.settings')
    # django.setup()

    # 创建一个Celery类的实例对象,虚拟机redis 8号数据库
    app = Celery('celery_tasks.tasks', broker='redis://192.168.124.10:6379/8')


    # # 定义任务函数
    # 定义任务函数
    @app.task
    def send_register_active_email(to_email, username, token):
        '''发送激活邮件'''
        # 组织邮件信息
        subject = '天天生鲜欢迎信息'
        message = ''
        sender = settings.EMAIL_FROM
        receiver = [to_email]
        html_message = '<h1>%s, 欢迎您成为拾忆医药会员</h1>请点击下面链接激活您的账户<br/><a href="http://127.0.0.1:8000/user/active/%s">http://127.0.0.1:8000/user/active/%s</a>' % (
        username, token, token)

        send_mail(subject, message, sender, receiver, html_message=html_message)
        time.sleep(5)

    #user/views.py
    class RegisterView(View):
        """ 注册 """

        ······

            # 发邮件
            send_register_active_email.delay(email, username, token)
            # 返回应答，跳转到首页
            return redirect(reverse('goods:index'))
## 三、登录视图的实现
**·** user/views.py
    class LoginView(View):
        """ 登录 """

        def get(self, request):
            # 当为get请求时
            return render(request, 'login.html')

        def post(self, request):
            # 当为post请求时
            username = request.POST.get('username')
            password = request.POST.get('pwd')
            # 校验数据
            if not all([username, password]):
                return render(request, 'login.html', {'errormsg': '数据不完整'})
            # 业务处理-登录校验
            # 使用 authenticate() 来验证用户。它使用 username 和 password 作为参数来验证，对每个身份验证后端( authentication backend ` )进行检查。
            # 如果后端验证有效，则返回一个 :class:`~django.contrib.auth.models.User 对象。如果后端引发 PermissionDenied 错误，将返回 None。
            user = authenticate(request, username=username, password=password)
            print('user_is:', user)
            if user is not None:
                # 不为空则用户名密码正确
                if user.is_active:
                    # 用户已激活
                    # 记住用户登录状态， login函数会在session中保存用户id，详情见文档：
                    # https://docs.djangoproject.com/zh-hans/3.1/topics/auth/default/
                    login(request, user)
                    return redirect(reverse('goods:index'))
                else:
                    # 用户账户未激活
                    return render(request, 'login.html', {'errormsg': '用户账户未激活'})
            else:
                # 用户名或密码错误
                return render(request, 'login.html', {'errormsg': '用户名或密码错误，请正确输入并去邮箱内激活！'})
## 四、配置redis作为django缓存和session后端
#### 1.安装并配置
**·** 安装django-redis库
                
    pip install django-redis
                
**·** 配置（https://django-redis-chs.readthedocs.io/zh_CN/latest/）
**·** settings.py添加如下配置：
                
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://192.168.153.128:6379/9", # 同celery 所用的redis ip
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            }
        }
    }

    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_CACHE_ALIAS = "default"

**·** 重新登录即可在redis数据库内查询session信息
    # 连接
    redis-cli -h 192.168.153.128
    # 选择数据库
    select 9
    # 显示全部
    KEYS *

    # 另外redis配置文件第69行，需要改成和celery一样的ip
        vim /etc/redis/redis.conf
#### 2.记住用户名

## 五、个人中心的实现
    **1** 记住用户名
    **2** 父模板页抽象
    **3** 用户中心页面显示
    **4** 登录装饰器及登录后跳转
    **5** 登录后的欢迎信息及退出登录
    **6** 用户中心---地址页
    **7** 模型管理器类方法封装
    **8** 用户中心---个人信息页
    **9** 历史记录存储格式设计及获取历史记录
    ## 六、fastdfs文件系统及Nginx安装配置
    **·** 海量存储、存储容扩展方便；解决文件内容重复问题；结合nginx提高网站提供图片的效率。
    **·** 文件：
    **·** 暂时无法在飞书文档外展示此内容
                
**1** 安装Fastdfs
                
    # 一、安装fastdfs依赖包
    1. 解压缩libfastcommon-master.zip
    2. 进入到libfastcommon-master的目录中
    3. 执行./make.sh
    4. 执行sudo ./make.sh install

    # 二、安装fastdfs
    1. 解压缩fastdfs-master.zip
    2. 进入到 fastdfs-master目录中
    3. 执行 ./make.sh
    4. 执行 sudo ./make.sh install

    # 三、配置跟踪服务器tracker
    1. sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf
    2. 在/home/python/目录中创建目录 fastdfs/tracker       
        mkdir –p /home/python/fastdfs/tracker
    3. 编辑/etc/fdfs/tracker.conf配置文件
        sudo vim /etc/fdfs/tracker.conf
    修改：base_path=/home/python/fastdfs/tracker

    # 四、配置存储服务器storage
    1. sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf
    2. 在/home/python/fastdfs/ 目录中创建目录storage
            mkdir –p /home/python/fastdfs/storage
    3. 编辑/etc/fdfs/storage.conf配置文件  
        sudo vim /etc/fdfs/storage.conf
    修改内容：
    base_path=/home/python/fastdfs/storage
    store_path0=/home/python/fastdfs/storage
    tracker_server=自己ubuntu虚拟机的ip地址:22122

    # 五、启动tracker 和 storage
    sudo service fdfs_trackerd start
    sudo service fdfs_storaged start

    # 六、测试是否安装成功
    1. sudo cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf
    2. 编辑/etc/fdfs/client.conf配置文件  sudo vim /etc/fdfs/client.conf
    修改内容：
    base_path=/home/python/fastdfs/tracker
    tracker_server=自己ubuntu虚拟机的ip地址:22122
    3. 上传文件测试：
    fdfs_upload_file /etc/fdfs/client.conf 要上传的图片文件  
    如果返回类似group1/M00/00/00/rBIK6VcaP0aARXXvAAHrUgHEviQ394.jpg的文件id则说明文件上传成功
**2** 安装Nginx
                
    1.Ubuntu安装前必备的依赖
        sudo apt-get install libpcre3 libpcre3-dev
        sudo apt-get install zlib1g-dev
        sudo apt-get install openssl libssl-dev
    2.解压并添加模块                                      
        (1)解压缩nginx-1.8.1.tar.gz、fastdfs-nginx-module-master.zip
        (2)进入nginx-1.8.1目录中
        (3)执行下面代码：
        sudo ./configure --prefix=/usr/local/nginx/ --add-module=fastdfs-nginx-module-master解压后的目录的绝对路径/src
    3.编译
        sudo make
    4.安装
        sudo make install
    5.复制配置文件并修改位置
        sudo cp fastdfs-nginx-module-master解压后的目录中src下的mod_fastdfs.conf  /etc/fdfs/mod_fastdfs.con
    6.编辑mod_fastdfs.conf配置文件
        sudo vim /etc/fdfs/mod_fastdfs.conf
        修改内容：
            connect_timeout=10
            tracker_server=自己ubuntu虚拟机的ip地址:22122
            url_have_group_name=true
            store_path0=/home/python/fastdfs/storage
    7. sudo cp 解压缩的fastdfs-master目录中的http.conf  /etc/fdfs/http.conf
    8. sudo cp 解压缩的fastdfs-master目录中的mime.types /etc/fdfs/mime.types
    9.sudo vim /usr/local/nginx/conf/nginx.conf
    在http部分中添加配置信息如下(第一行加入user root;)：
    server {
                listen       8888;
                server_name  localhost;
                location ~/group[0-9]/ {
                    ngx_fastdfs_module;
                }
                error_page   500 502 503 504  /50x.html;
                location = /50x.html {
                root   html;
                }
            }
    10. 启动nginx
    sudo /usr/local/nginx/sbin/nginx



    # 启动celery静态页面的时候，添加的如下配置项
    cd /usr/local/nginx

    vim conf/nginx.conf
    # 添加如下内容
     server {
            listen       80;
            server_name  localhost;

            #charset koi8-r;

            #access_log  logs/host.access.log  main;
            location /static{
                alias /home/chenglong/chenglong/SYDrug/static/;
            }
            location / {
                root   /home/chenglong/chenglong/SYDrug/static/;
                index  index.html index.htm;
            }
    ...

    # 重启nginx
    sudo /usr/local/nginx/sbin/nginx -s reload

    ps aux | grep nginx

#### 3.代码部分
**1**  编写utils/fdfs/storage.py类
                
    from django.core.files.storage import Storage
    from django.conf import settings
    from fdfs_client.client import Fdfs_client, get_tracker_conf


    class FDFSStorage(Storage):
        """fast dfs文件存储类"""

        def __init__(self, client_conf=None, base_url=None):
            """初始化"""
            if client_conf is None:
                # client_conf = settings.FDFS_CLIENT_CONF
                # 这里一定要写绝对路径，同时，进入get_tracker_conf方法中，也修改为绝对路径
                client_conf = get_tracker_conf(
                    'C:/Users/chenglong/Desktop/SYDrug/utils/fdfs/client.conf')
            self.client_conf = client_conf

            if base_url is None:
                base_url = settings.FDFS_URL
            self.base_url = base_url

        def _open(self, name, mode='rb'):
            """打开文件时使用"""
            pass

        def _save(self, name, content):
            """保存文件时使用"""
            # name:你选择上传文件的名字
            # content:包含你上传文件内容的File对象

            # 创建一个Fdfs_client对象
            client = Fdfs_client(self.client_conf)

            # 上传文件到fast dfs系统中
            res = client.upload_by_buffer(content.read())
            # dict
            # {
            #     'Group name': group_name,
            #     'Remote file_id': remote_file_id,
            #     'Status': 'Upload successed.',
            #     'Local file name': '',
            #     'Uploaded size': upload_size,
            #     'Storage IP': storage_ip
            # }.

            if res.get('Status') != 'Upload successed.':
                # 上传失败
                raise Exception('上传文件到fast dfs失败')

            # 获取返回的文件ID
            filename = res.get('Remote file_id')

            return filename.decode()

        def exists(self, name):
            """Django判断文件名是否可用"""
            return False

        def url(self, name):
            """返回访问文件的url路径"""
            return self.base_url + name
#### 2. 添加setting.py文件配置
    # 设置Django的文件存储类
    DEFAULT_FILE_STORAGE = 'utils.fdfs.storage.FDFSStorage'
#### 3. 注册超级管理员账户，在后台管理系统查看是否可以上传成功
    # 注册superuser账户
        python manage.py createsuperuser
    # goods/admin.py中添加如下代码：
        from django.contrib import admin
        from ..goods.models import GoodsType
        # Register your models here.

        admin.site.register(GoodsType)
    # 登录admin添加查看
        python manage.py runserver
        # 1.遇到上传失败 client.py第51行错误的时候
        # https://blog.csdn.net/Jacky_kplin/article/details/103014800
        解决方法：
        原代码中（storage.py）的client_conf = settings.FDFS_CLIENT_CONF注释掉
        换成client_conf = get_tracker_conf(r'C:\Users\chenglong\Desktop\SYDrug\win_env\Lib\site-packages\fdfs_client\client.conf')
    # 遇到上传其他错误，例如超时时间未配置，字符类型不匹配，尝试decode()文件名和替换绝对路径
    # https://blog.csdn.net/Jacky_kplin/article/details/103014112
    # https://blog.csdn.net/Moelimoe/article/details/114339517
## 七、商品模块
    # 添加购物车数量
    # Ubuntu下进行如下操作：
    # 打开redis数据库
    redis-cli -h 192.168.124.10
    # 选择9号数据库
    select 9
    # 显示全部数据
    keys *
    # 设置cart_2测试数据
    hmset cart_2 1 3 2 5
    # 数据库中查询，返回值为：（interger)2
    HLEN cart_2

**·** goods/views.py中添加如下代码：
                
    # 获取用户购物车中商品数目
    user = request.user
    cart_count = 0
    if user.is_authenticated:
        # 用户已登录
        conn = get_redis_connection('default')
        cart_key = 'cart_%i' % user.id
        cart_count = conn.hlen(cart_key)
                
**·** base.html中做如下修改，仅加一条模板语法即可
    <div class="guest_cart fr">
        <a href="#" class="cart_name fl">我的购物车</a>
        <div class="goods_count fl" id="show_count">{{ cart_count }}</div>
    </div>
## 八、全局检索
**1** 安装django-heystack
                
    # 在虚拟环境内安装
        pip install django-heystack
        pip install whoosh
    # 在settings.py文件中注册应用,并添加配置文件
    [图片]
    生成索引文件
    创建如下目录结构和文件：
    [图片]
**·** 创建search.html文件
                
    {% extends 'base_detal_list.html' %}
    {% block title %}天天生鲜-商品搜索结果列表{% endblock title %}
    {% block main_content %}
       <div class="breadcrumb">
          <a href="#">{{ query }}</a>
          <span>></span>
          <a href="#">搜索结果如下:</a>
       </div>

       <div class="main_wrap clearfix">
            <ul class="goods_type_list clearfix">
                {% for item in page %}
                <li>
                    <a href="{% url 'goods:detail' item.object.id %}"><img src="{{ item.object.image.url }}"></a>
                    <h4><a href="{% url 'goods:detail' item.object.id %}">{{ item.object.name }}</a></h4>
                    <div class="operate">
                        <span class="prize">￥{{ item.object.price }}</span>
                        <span class="unit">{{ item.object.price}}/{{ item.object.unite }}</span>
                        <a href="#" class="add_goods" title="加入购物车"></a>
                    </div>
                </li>
                {% endfor %}
            </ul>
            <div class="pagenation">
                    {% if page.has_previous %}
                <a href="/search?q={{ query }}&page={{ page.previous_page_number }}"><上一页</a>
                    {% endif %}
                    {% for pindex in paginator.page_range %}
                        {% if pindex == page.number %}
                        <a href="/search?q={{ query }}&page={{ pindex }}" class="active">{{ pindex }}</a>
                        {% else %}
                        <a href="/search?q={{ query }}&page={{ pindex }}">{{ pindex }}</a>
                        {% endif %}
                {% endfor %}
                    {% if spage.has_next %}
                <a href="/search?q={{ query }}&page={{ page.next_page_number }}">下一页></a>
                    {% endif %}
             </div>
       </div>
    {% endblock main_content %}
**·** 生成索引文件：位置在项目根目录下的文件夹内：whoosh_index
           
    (win_env) PS C:\Users\chenglong\Desktop\SYDrug> python .\manage.py rebuild_index

**3** 修改分词方式

    # 1. 安装jieba分词模块。
        pip install jieba
    # 2. 找到虚拟环境py_django下的haystack目录。
    C:\Users\chenglong\Desktop\SYDrug\win_env\Lib\site-packages\haystack\backends\
    # 3. 在上面的目录中创建ChineseAnalyzer.py文件。
    import jieba
    from whoosh.analysis import Tokenizer, Token

    class ChineseTokenizer(Tokenizer):
        def __call__(self, value, positions=False, chars=False,
                     keeporiginal=False, removestops=True,
                     start_pos=0, start_char=0, mode='', **kwargs):
            t = Token(positions, chars, removestops=removestops, mode=mode, **kwargs)
            seglist = jieba.cut(value, cut_all=True)
            for w in seglist:
                t.original = t.text = w
                t.boost = 1.0
                if positions:
                    t.pos = start_pos + value.find(w)
                if chars:
                    t.startchar = start_char + value.find(w)
                    t.endchar = start_char + value.find(w) + len(w)
                yield t

    def ChineseAnalyzer():
        return ChineseTokenizer()


**4** 复制whoosh_backend.py文件，改为如下名称。

    whoosh_cn_backend.py
    
**5** 打开复制出来的新文件，引入中文分析类，内部采用jieba分词。
    from .ChineseAnalyzer import ChineseAnalyzer
    
**·** 更改词语分析类。

    # 查找
        analyzer=StemmingAnalyzer()
    # 改为
    # --------------------------------------
        analyzer=ChineseAnalyzer()
    #查找
        analyzer=StemmingAnalyzer()
    #改为
        analyzer=ChineseAnalyzer()
**6** 修改settings.py文件中的配置项。
           
**·** 全文检索框架的配置
    HAYSTACK_CONNECTIONS = {
        'default': {
            # 使用whoosh引擎
            # 'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
            'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
            # 索引文件路径
            'PATH': os.path.join(BASE_DIR, 'whoosh_index'),
        }
    }

**·** 当添加、修改、删除数据时，自动生成索引
    HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

**7** 重新生成索引文件
    (win_env) PS C:\Users\chenglong\Desktop\SYDrug> python .\manage.py rebuild_index


#### 九、pyecharts绘图
           
**1** 首先采用饼状图测试，如下以pymysql为例进行测试，后续通过django orm模型实现
**·** 创建新app应用 charts，图表url配置为:chats/chat
**·** settings.py文件中配置后台菜单
  
    import pymysql
    from pyecharts import options as opts
    from pyecharts.charts import Pie

    connection = pymysql.connect(
        host='localhost',
        port=3306,
        user='chenglong',
        password='123456',
        database='SYDrug'
    )

    with connection.cursor() as cursor:
        # 查询商品SPU和销量
        sql = "SELECT name, sales FROM df_goods_sku"
        cursor.execute(sql)
        results = cursor.fetchall()
        # 将商品SPU和销量分别存储到不同列表中
        goods = []
        sales_list = []
        for row in results:
            goods.append(row[0])
            sales_list.append(row[1])

    connection.close()

    # print(goods)
    # print(sales_list)
    # 将两个列表合并为一个二元组列表
    data = [(goods[i], sales_list[i]) for i in range(len(goods))]

    # 创建饼状图示例
    pie_chart = Pie()

    # 配置饼状图参数
    pie_chart.set_global_opts(
        title_opts=opts.TitleOpts(title="商品销量饼状图"),
        legend_opts=opts.LegendOpts(orient="vertical", pos_top="15%", pos_left="80%"),
    )

    # 添加饼状图数据
    pie_chart.add(
        "",
        data_pair=data,
        radius=["40%", "60%"],
        center=["30%", "50%"],
        label_opts=opts.LabelOpts(
            position="outside",
            formatter="{b}: {c} ({d}%)"
        ),
    )
    # 显示饼状图
    pie_chart.render('mychart.html')

**2** 更新后台数据库数据，图表会自动更新
    update df_goods_sku set sales=500 where name='布洛芬缓释胶囊';
#### N、报错及解决：
           
**1** Ubuntu安装mysqlclient失败：
           
    https://blog.csdn.net/panzer9/article/details/52870701/
    # 安装缺失的库
        sudo apt-get install libmysqlclient-dev
        sudo apt-get install python3-dev
        # 缺失wheel则安装下面
        pip install wheel
        # 缺失mysqlDB或者_mysql问题，则
        sudo apt install libmysqlclient21

**2** redis配置(ubuntu)：
           
    1. 首先进入redis配置文件（sudo vi /etc/redis/redis.conf）,ip地址通过ifconfig查看
        注释原有bind，新加如下：
            # bind 127.0.0.1 ::1
            bind 192.168.124.10 ::1
        关掉守护模式：
            protected-mode no
            daemonize no
    2. 重启redis
        service redis restart
    3. ps aux | grep 'redis',可以查看redis进程。

    # 服务器打开6379端口
    sudo ufw allow 6379
           
**3** Nginx安装过程中出现make错误一
           
    1.执行make时候出现错误，例如：
        ^~~~
        cc1: all warnings being treated as errors
        make[1]: *** [objs/Makefile:473: objs/src/core/ngx_murmurhash.o] Error 1
        make[1]: Leaving directory ‘/root/nginx-1.10.1‘
        make: *** [Makefile:8: build] Error 2
        ————————————————
    解决办法：
            是将警告当成了错误处理，打开 nginx的安装目录/objs/Makefile，去掉CFLAGS中的-Werror，再重新make。
        -Wall 表示打开gcc的所有警告  
        -Werror，它要求gcc将所有的警告当成错误进行处理
           
**4** Nginx安装过程中出现make错误二
           
    src/os/unix/ngx_user.c: In function ‘ngx_libc_crypt’:
    src/os/unix/ngx_user.c:36:7: error: ‘struct crypt_data’ has no member named ‘current_salt’
    cd.current_salt[0] = ~salt[0];
    ^
    make[1]: *** [objs/Makefile:774: objs/src/os/unix/ngx_user.o] Error 1
    make[1]: Leaving directory ‘/root/nginx-1.10.1‘
    make: *** [Makefile:8: build] Error 2
    ————————————————
    解决办法：
    这里提示我们struct crypt_data’没有名为‘current_salt’的成员：cd.current_salt[0] = ~salt[0]；
    最好的办法是换一个版本，因为条件限制，我们就进到源码里把这行直接注释掉好了。
    # vim src/os/unix/ngx_user.c进入里面注释掉36行：

    /* cd.current_salt[0] = ~salt[0];*/
           
**5** Nginx+FastDFS访问文件没有权限/404错误
           
    在已备份的nginx.conf文件第一行指定用户名即可
        user root;
    以下内容也操作过，不知道对不对
        对storage的存储文件夹执行755权限，原来是700
           
**6** 模板中传递{{sku.count}}的时候，前端显示类型为字节类型 b'2'
           
    在Django模板中，使用|int进行类型转换是可行的，但是需要确认使用的Django版本是否支持该过滤器。在Django 3.1及以下版本中，int过滤器是不存在的，因此在模板中使用|int会导致模板语法错误。如果你的Django版本较旧，可以尝试使用|floatformat过滤器进行类型转换，例如：
    arduinoCopy code
    {{ sku.count|default:"0"|floatformat }}
    在这个示例中，使用floatformat过滤器将变量转换为浮点数类型。如果你的变量本身就是整数类型，那么使用该过滤器进行类型转换也是可行的。如果你的Django版本支持int过滤器，也可以使用|int进行类型转换。
           
**7** 并发问题
           
    目前未在windows数据库中开启事务的隔离级别（读-已提交）：
        mysql的 traceaction-isolatio设置为：READ-COMMITED
           
**8** 订单创建数据表出现问题，重新执行下面代码段
           
    DROP TABLE IF EXISTS `df_order_info`;
    CREATE TABLE `df_order_info` (
      `create_time` datetime(6) NULL DEFAULT NULL,
      `update_time` datetime(6) NULL DEFAULT NULL,
      `is_delete` tinyint(1) NOT NULL,
      `order_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
      `pay_method` smallint(0) NOT NULL,
      `total_count` int(0) NOT NULL,
      `total_price` decimal(10, 2) NOT NULL,
      `transit_price` decimal(10, 2) NOT NULL,
      `order_status` smallint(0) NOT NULL,
      `trade_no` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
      `addr_id` int(0) NOT NULL,
      `user_id` int(0) NOT NULL,
      PRIMARY KEY (`order_id`) USING BTREE,
      INDEX `df_order_info_addr_id_70c3726e_fk_df_address_id` (`addr_id`) USING BTREE,
      INDEX `df_order_info_user_id_ac1e5bf5_fk_df_user_id` (`user_id`) USING BTREE,
      CONSTRAINT `df_order_info_addr_id_70c3726e_fk_df_address_id` FOREIGN KEY (`addr_id`) REFERENCES `df_address` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
      CONSTRAINT `df_order_info_user_id_ac1e5bf5_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;


    DROP TABLE IF EXISTS `df_order_goods`;
    CREATE TABLE `df_order_goods` (
      `id` int(0) NOT NULL AUTO_INCREMENT,
      `create_time` datetime(6) NULL DEFAULT NULL,
      `update_time` datetime(6) NULL DEFAULT NULL,
      `is_delete` tinyint(1) NOT NULL,
      `count` int(0) NOT NULL,
      `price` decimal(10, 2) NOT NULL,
      `comment` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
      `order_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
      `sku_id` int(0) NOT NULL,
      PRIMARY KEY (`id`) USING BTREE,
      INDEX `df_order_goods_order_id_6958ee23_fk_df_order_info_order_id` (`order_id`) USING BTREE,
      INDEX `df_order_goods_sku_id_b7d6e04e_fk_df_goods_sku_id` (`sku_id`) USING BTREE,
      CONSTRAINT `df_order_goods_order_id_6958ee23_fk_df_order_info_order_id` FOREIGN KEY (`order_id`) REFERENCES `df_order_info` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
      CONSTRAINT `df_order_goods_sku_id_b7d6e04e_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
    ) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;


#### M、项目启动流程
           
**1** 创建虚拟环境
**·** windows下进入项目根目录
           
    # 创建虚拟环境
        python -m venv venv
    # 进入虚拟环境
        ./venv/Script/activate
    # 安装项目包
        pip install -r requirements

**·** Linux下
           
    # 创建虚拟环境
        python3 -m venv sy_env
    # 进入虚拟环境
        source ./sy_env/bin/activate
    # 安装项目包
        pip install -r requirements
           
**2** 配置数据库文件
           
    # 创建数据库(sql下执行)：
        create database SYDrug charset=utf8;
    # 生成数据表及迁移文件(项目根目录）
        python manange.py makemigrations
        python manage.py migrate
           
**3** 启动Celery及项目
           
    # 启动redis
        sudo service redis-server start
    # 查看是否启动成功
        sudo netstat -lnp | grep redis
        redis-cli -h 本机ip

    # 任务处理者一端（Ubuntu），项目根目录下启动：
        celery -A celery_tasks.tasks worker -l info

    # 启动fds
        sudo service fdfs_trackerd start
        sudo service fdfs_storaged start

    # 本机启动项目：
        python manage.py runserver
           
#### Q、项目最新代码
    Github:
    ## Github链接
    Github：https://github.com/3148508410/SYDrug/tree/dev

    ## ssh获取（需要添加ssh密钥）
    git clone git@github.com:3148508410/SYDrug.git

    ## 本地修改同步至github(dev分支)
    git add templates/base.html 
    git commit -m '修改后台跳转方式'
    git push -u origin dev

    ##其他命令：
    查看状态：git status

    查看修改情况：git diff

    列出本地全部分支：git branch

    获取dev分支的最新修改：git pull origin dev

    切换到main分支：git checkout main

    合并分支：git merge
    示例：将开发分支合并到主分支：
        git checkout master
        git merge dev
