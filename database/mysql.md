# 开启root所有权限 
> 进入到MySQL use mysql; GRANT ALL PRIVILEGES ON . TO 'root'@'%' IDENTIFIED BY 'hillstone'; flush privileges; 
> 操作命令 mysql -uroot -phillstone 执行这个命令进入数据库 
>* show databases; 显示所有的数据库 
>* create database name;创建数据库 
>* use database_name; 进入到这个数据库中
>* show tables; 显示这个数据库下的所有表 
>* select * from tables; 从选定的表下面筛选数据 
>* concat 可以给查询到结果前面添加字符串，改变查询结果 
>* ALTER TABLE table_name ADD field_name type; 给某个表添加某个字段 
>* ALTER TABLE table_name DROP field_name 删除表的某个字段

当创建一个数据库没有成功的时候要注意是不是root权限，或者有没有给当前用户相应的权限。如果没有，方法如下：

>* 创建一个新表 create table commodity_comments (id VARCHAR(10),commodity_id VARCHAR(10),user_id VARCHAR(10),commonts VARCHAR(255),CUP VARCHAR(8),PRIMARY KEY (id));
>* 查看数据库的所有属性 desc 
>* 删除数据库中的某张表 drop table 
>* 更改数据库的权限 grant all privileges on database_name.* to user@localhost identified by password; grant all privileges on . to user@localhost identified by password;
>* 给用户所有数据库的所有权限 更数据库中某一列的数据 UPDATE table_name set set_name=" "
>* 删除表中的所有数据 truncate table name

>* mysql自增列的增加方式 show variables like "auto_increment_offset" auto_increment_offset + N × auto_increment_increment N表示第几次，从1开始计算

# mysql没有长连接 
> 注意在使用数据库的时候，一定要注意没有长连接，只有短链接，连接到一定的时间就会超时，断掉。所以在使用的时候要注意，在写入数据库之前要关注一下与数据库的连接是否断掉。如果断掉，注意重连。
