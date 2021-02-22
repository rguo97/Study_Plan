# nginx服务器
## 介绍
> Nginx是一个HTTP和反向代理服务器，并发能力强，最多能支持高达50000个连接并发数。他主要被用来实现正向代理，反向代理，负载均衡已经动静分离这四个功能

## 正向代理
> 我们先发送请求到我们的代理服务器，然后代理服务器再去请求Google的服务器，最后将请求到的内容返回给我们本机。而这样一种模式呢，我们就称之为正向代理。

## 反向代理
> 代理服务器会把服务器隐藏起来，当client的请求发往server的时候，经过代理服务器的时候，会把请求通过负载均衡分发下去，从而隐藏真正的IP。反向代理服务器和目标服务器对外就是一个服务器，暴露的是代理服务器 地址，隐藏了真实服务器 IP 地址。

```
server {
        listen       8888 ; ##设置我们nginx监听端口为8888
        server_name  [服务器的ip地址];

        # Load configuration files for the default server block.
        include /etc/nginx/default.d/*.conf;

        location /hi/ {
            proxy_pass http://127.0.0.1:8080; ##需要代理的服务器地址
            index index.html;
        }
        
        location /hello/ {
            proxy_pass http://127.0.0.1:8081; ##需要代理的服务器地址
            index index.html;
        }

        error_page 404 /404.html;
            location = /40x.html {
        }

        error_page 500 502 503 504 /50x.html;
            location = /50x.html {
        }
```
# 负载均衡

# 动静分离

https://github.com/hanshuaikang/HanShu-Note/blob/master/Nginx%E5%88%9D%E7%BA%A7%E5%85%A5%E9%97%A8%E6%95%99%E7%A8%8B/%E5%86%99%E7%BB%99%E5%90%8E%E7%AB%AF%E7%9A%84Nginx%E5%88%9D%E7%BA%A7%E5%85%A5%E9%97%A8%E6%95%99%E7%A8%8B%E5%AE%9E%E6%88%98%E7%AF%87.md#%E4%B8%8B%E9%9D%A2%E5%BC%80%E5%A7%8B%E6%8A%80%E6%9C%AF%E6%80%BB%E7%BB%93



## nginx命令

```
service nginx start/stop/restart
    
#查看nginx安装路径
nginx -t
#查看nginx的相关版本信息
nginx -v
#验证配置文件的正确性
nginx -T
#重新加载配置文件
nginx -s reload
```

## nginx结构
### 全局块  
> 关于nginx的一些全局配置文件，进程数，进程PID存放的位置，错误日志等
### events块
### http块  
> http 全局块配置的指令包括文件引入、MIME-TYPE定义、日志自定义、连接超时时间、单链接请求数上限等。而http块中的server块则相当于一个虚拟主机，一个http块可以拥有多个server块。

### server块
> 又包括全局server块，和location块。有一个主要的配置文件。其他的会覆盖配置文件。允许哪些主机访问，不允许哪些。

```
    server  {
       listen 80 default;
       server_name _;
       #server_name www.rguo97.com rguo97.com
       return 404;
    }
```


## HTTP服务的默认配置
```
    #位置：
    /etc/nginx/nginx.conf
    # worker以什么身份运行
    user  nginx; // default nobody

    # worker进程个数，一般为 CPU 个数，也可选 auto
    worker_processes  1; # default 1

    # 每个worker可打开的描述符限制
    worker_rlimit_nofile 8192;

    # 错误日志保存路径和级别
    error_log  /var/log/nginx/error.log warn;

    # 进程pid保存路径
    pid        /var/run/nginx.pid;

    # 指定dns服务器
    resolver 10.0.0.1;

    events {
        # 每个worker最大连接数
        worker_connections  1024; # default 1024
    }

    # http 服务定义
    http {
        # 加载 mime 类型
        include       /etc/nginx/mime.types;
        # 定义默认数据类型
        default_type  application/octet-stream;
        # 日志格式
        log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                          '$status $body_bytes_sent "$http_referer" '
                          '"$http_user_agent" "$http_x_forwarded_for"';
        # 访问日志
        access_log  /var/log/nginx/access.log  main;
        # 是否调用sendfile函数（zero copy 方式）来输出文件，如果磁盘IO重负载应用，可设置为off
        sendfile        on;
        # 此选项允许或禁止使用socke的TCP_CORK的选项，此选项仅在使用sendfile的时候使用
        #tcp_nopush     on;

        keepalive_timeout  65;

        # 代理相关设置
        # proxy_connect_timeout 90;
        # proxy_read_timeout 180;
        # proxy_send_timeout 180;
        # proxy_buffer_size 256k;
        # proxy_buffers 4 256k;
        # proxy_busy_buffers_size 256k;
        # proxy_temp_file_write_size 256k;

        # tcp_nodelay on;
    
        # gzip 压缩
        #gzip  on;

        # 加载其它配置，这样我们在 conf.d 下写的文件才会生效
        include /etc/nginx/conf.d/*.conf;
    }

```

# 消息队列rabbitmq
>* https://segmentfault.com/a/1190000014041428
>* https://www.jianshu.com/p/dae5bbed39b1
>* https://www.cnblogs.com/sanduzxcvbnm/p/11309255.html





