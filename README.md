# user
使用flask-httpauth，flask-sqlalchemy，flask-migrate实现的简单用户登入认证

# 关于登陆

由自己实现的user表，然后自己处理好registe和login的表单，

尽量不用`basic_auth`，因为不安全，而且没有防暴力破解的措施

login成功后可以返回token，后续都用token认证除非需要更新token

# 关于权限管理

采用Permission记录相关权限级别，然后绑定到Role的数据库表中，

User表再绑定Role，这样user就可以有role的权限，里面的permission可以为单个，也可以为多个

admin默认拥有所有权限，所以在user的can判断中，判断isAdmin就都返回True

另外，如果要确认只有文档的所有者才有的权限，可以在路由函数中自己判断是否为文档所有者
