# -*- coding: GBK -*-
#------------------------------------------
#   Author: clzqwdy@gmail.com
#
#   Logs:
#   2010-02-27: achieve basic framework and functions
#   2010-03-12: get a single contact
#   2010-03-13: get full contacts
#   2010-03-15: store all contacts, by 'for'
#   2010-03-16: framework of MainPage
#   2010-03-17: delete rpc.py and add it into infosec.py
#               basic contacts.html display
#               create base.html and modify other html by using Django templates
#               slove encoding problem
#               in contacts.html, display data in table form
#   2010-03-18: 插入数据时应该检查已经存在，即在BackUpHandler中(先不做了)
#               login in different mobile, create LoginHandler
#               test in Windows Mobile, create TestHandler
#               main finish LoginHandler
#   2010-03-19: 再次修改数据表的设计，使用References
#               response with a KEY in LoginHandler
#               根据KEY, 修改BackupHandler的机制
#               完善了HTML前台页面的框架，并给王琴安排了任务
#               添加了KEY后，ContactPage出现问题了，neet to add some functions
#   2010-03-20: solve ['unicode' object has no attribute 'has_key'] in ContactPage
#               according KEY, read specifical contacts out in ContactPage
#   2010-03-22: 1. solve [AttributeError: 'NoneType' object has no attribute 'email']
#               in ContactPage, 就是不登陆的状态下直接访问/contact会出错
#               但是为什么在Lock页面中是跳转的呢?
#               2. 重新处理各个链接之间的关系，如果是未登录的状态访问，则跳转到google
#               in all pages, add [self.redirect(url)]
#               3. write BackupPage
#               4. newly add WipePage, SmsPage, CallLogPage
#               5. modify MainPage and index.html
#               6. spend a lot of time modifing CSS with WangQin
#               7. add form in backup.html, and newly add BackupAction
#               表单的处理还是不大会啊！
#               8. add class CmdHandler and class Cmd(db.Model)
#   2010-03-23: 1. handle form in BackupAction by post
#               修改王琴写的表单中的value，这个可是要传过去的，怎么能用英文呢
#               post请求提交过去的数据显示成功
#               2. handle form in BackupAction by get
#               use Google Code Search's [getRequestParams]
#   2010-03-24: 1. add datastore operator in BackupAction
#               have problem in KEY
#               2. modify wipe.html's form
#               3. rename 'BackupAction' to 'CmdAction'
#               4. modify 'MainPage': 未登录的状态下访问首页出错，增加到if user条件下
#               5. backup页面不跳转，wipe页面跳转, python中的switch-case如何写
#               6. modify lock.html and simply LockPage
#   2010-03-27: 1. newly add 'CallLogHandler', newly add 'CallLog'
#               basic achieve 'CallLogHandler'
#               2. modify 'CallLogPage' and calllog.html
#               3. newly add 'SmsHandler', newly add 'Sms' datastore
#               4. modify 'SmsPage' and sms.html
#   2010-04-05: 1. 增加了cmd.html
#               2. 在CmdAction中增加命令的前台显示
#   2010-04-06: 1. modify 'CmdHandler': 客户端到这里来反馈指令的完成
#   2010-04-08: 1. add class 'StateHandler'
#   2010-04-09: 1. '/action/cmd.do'改为'/cmd.do'
#   2010-04-10: 1. 解决了：当通讯录为空时，/contact会有问题！
#               2. modify class LoginHandler to get 'sim'
#   2010-04-11: 1. index.html增加当前SIM卡号的显示，在class MainPage中
#               2. 重新设计class Login表，增加注册时的手机号！
#               3. modify class CmdAction，增加对lock指令的处理
#               4. modify all html's title 'xx - MobileSecure'
#               5. 在Phone表中增加time属性，这样方便unlock的指令反馈，就只用删除cmd中的记录了，不用去更改Phone表中的记录了！
#               6. class LoginHandler中初始化Phone表
#               7. 在class LockPage中使用Query接口，放弃使用GqlQuery
#               8. 发现需要增加索引
#   2010-04-30: 1. 修改app.yaml，增加secure参数。但是我们不应该轻易使用这个参数，因为这会增加负担。
#
#   Todo:
#   2. 资源不存在的那个码是404吗？
#   done! 3. 将来参加全国信安大赛，能不能以飞信的方式来替代短信猫的方式
#   4. 一行不够，如何分行写？
#   5. 叫王琴和我一起搞Ajax
#   must! 6. 首页在IE8.0下显示有严重问题
#   7. CmdAction中表单数据提交后变成404
#   done! 8. backup页面应该要和wipe页面区别大些，用户不太好分别是在哪个页面下啊
#   9. 叫王琴修改lock.html, 叫她看w3school
#   done! 10. 叫王琴，图片就拉伸到那么大，不要重复
#   11. 服务端各种操作都应该用https
#   done! 12. why '/sms' will have two [> >]?
#   must! 13. 通讯录一多，http://nupter-cn.appspot.com/contact就出现问题了，说明模板有问题
#   14. http://code.google.com/appengine/docs/python/datastore/keysandentitygroups.html中的class="prettyprint"用在我们的前台指令显示里
#   need! 15. 没有在手机客户端注册的用户，照理是不能登陆系统的，因为它会乱发指令啊，而Login表中是没有该用户的数据的。
#   done! 16. 当通讯录为空时，/contact会有问题！
#   17. index.html中显示SIM卡号时的样式！
#   18. 到底何时才需要用<div>
#
#   Reference:
#   http://code.google.com/appengine/docs/python/tools/webapp/redirects.html
#   http://code.google.com/appengine/docs/python/datastore/functions.html
#   http://code.google.com/appengine/docs/python/datastore/gqlreference.html
#------------------------------------------

# to use template, it is a python lib
import os
# to solve [NameError: global name 'urllib' is not defined]
import urllib

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template
from google.appengine.ext import db

from xml.dom import minidom

# right?
"""
class Total(db.Model):              # 总表，对应到每个客户端，所有的信息都能汇总到这
    email = db.StringProperty()
    pswd = db.StringProperty()
    contact = db.ReferenceProperty(Contact)         # 该手机中所有的通讯录
    lock = db.ReferenceProperty(Phone)              # current SIM and locking state
"""

class Login(db.Model):
    # maybe don't need it, because has a key in default
    #nid = db.StringProperty()
    email = db.StringProperty()
    pswd = db.StringProperty()
    sim = db.StringProperty()       # 用户注册时的手机号

class Phone(db.Model):              # lock table and current SIM
    # if I can use data type, better writing is:
    #nid = db.IntegerProperty()
    #num = db.IntegerProperty()
    #lock = db.BooleanProperty()
    
    #pswd = db.StringProperty()
    #location = db.StringProperty()
    
    # need to modify，可能要把表删除了，因为可能已经有数据了
    nid = db.ReferenceProperty(Login)           # KEY Properties
    #nid = db.StringProperty()
    num = db.StringProperty()                   # 当前SIM卡号，并不一定是原始的啊
    lock = db.StringProperty()                  # 是否锁定
    date = db.DateTimeProperty(auto_now_add=True)   # 上传这条记录时的时间

class Contact(db.Model):                        # backup table
    nid = db.ReferenceProperty(Login)           # KEY Properties
    name = db.StringProperty()                  # every contact's name
    # the same name doesn't matter in Python?
    phone = db.StringProperty()                 # every contact's phone
    
class CallLog(db.Model):
    nid = db.ReferenceProperty(Login)           # KEY Properties
    name = db.StringProperty()                  # person called
    number = db.StringProperty()
    type = db.StringProperty()                  # 是主叫还是被叫
    date = db.StringProperty()
    duration = db.StringProperty()              # 通话持续时间
    
class Sms(db.Model):
    nid = db.ReferenceProperty(Login)
    name = db.StringProperty()                  # <name>
    number = db.StringProperty()                # <number>
    date = db.StringProperty()                  # <date>
    body = db.StringProperty()                  # <body>
    
class Cmd(db.Model):                #
    # backup: 'b';
    # delete: 'd';
    # lock: 'l';
    # 0: contact, 1: sms, 2: calllog
    # so if backup sms, cmd is: 'b1'
    message = db.StringProperty()               # 包含命令的字符串
    nid = db.ReferenceProperty(Login)           # KEY Properties, 应该是那一条Entity

# just for test    
class LockDB(db.Model):
    strXML = db.StringProperty(multiline=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        # or use 'users.GetCurrentUser()'?
        user = users.get_current_user()
        
        if user:
            # 不写在判断语句前面，是为了效率问题，也是要报错的
            username = user.nickname()
            url = users.create_logout_url(self.request.uri)
            
            email = user.email()
            queryLogin = db.GqlQuery("SELECT * FROM Login WHERE email = :1", email )
            
            entity = queryLogin.get()
            #entity = queryLogin.fetch(1)
            #entitys = queryLogin     # 肯定只有一条嘛
            
            #sim = entity.sim   # 'NoneType' object has no attribute 'sim'
            
            ''' # still has no use
            if entity is None:
                flag = False
            else:
                flag = True
            '''
            
            # vals in templates
            template_values = {
                # which in .py file? which in template?
                # 按照python语法来说，显然后者是.py file里的
                'username': username,
                'url': url,
                #'sim': sim
                'entity': entity,
                #'entitys': entitys,
                #'flag': flag
            }
            
            path = os.path.join( os.path.dirname(__file__), 'templates/index.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )
        else:
            # http://localhost:8080/_ah/login?continue=http://localhost:8080/
            # display login page
            url = users.create_login_url(self.request.uri)
            self.redirect(url)

# display current SIM and it's locking state
class LockPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        
        # if not loginned, let user login first
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            email = user.email()
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            key = queryLogin.get()
            
            queryLock = db.GqlQuery("SELECT * FROM Phone WHERE nid = :1 " +
                                    "ORDER BY date DESC", key)
            lock = queryLock.get()
            
            ''' # 改用Query接口，靠！不用这么折腾，GqlQuery还是支持的！
            queryLock = Phone.all().filter('nid = ', key).order('-date')
            lock = queryLock.get()
            '''
            
            template_values = { 'lock': lock, 'email': email }
            
            path = os.path.join( os.path.dirname(__file__), 'templates/lock.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )
        
class BackupPage(webapp.RequestHandler):
    def get(self):
        # test chinese, must add ['Content-Type']
        #self.response.headers['Content-Type'] = 'text/html; charset=GBK'
        #self.response.out.write("test 中文")
        
        user = users.get_current_user()
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            template_values = { }
            path = os.path.join( os.path.dirname(__file__), 'templates/backup.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            # ws地使用了个空的模板值，应该有更好的办法！
            self.response.out.write( template.render(path, template_values) )
            
class WipePage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            template_values = { }
            path = os.path.join( os.path.dirname(__file__), 'templates/wipe.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )
 
# display Contact 
class ContactPage(webapp.RequestHandler):        # display contacts
    def get(self):
        user = users.get_current_user()
        
        # if not loginned, let user login first
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        
        # 如果不加else,会继续编译下去，但是用户看不出效果？yes
        else:
            # 不是第一次创建entity时，如何再获取它的KEY？
            # according to the Email, we get specifical KEY
            
            # 1.get email, test Success!
            email = user.email()
            # 2.query entity by email in Login Table
            # queryLogin must be a 'GqlQuery' object
            # the use of ancestor()?
            #queryLogin = db.GqlQuery("SELECT * FROM Login WHERE email = :1", email)
            
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # 下面的写法一般是可以的，但是如果某个用户在Login表中不存在就会error了
            #entity = queryLogin.fetch(1)
            #key = entity        # 还不是字符串型的，是个key path类型的吧？
            key = queryLogin.get()
            
            # test 'key' type: [datastore_types.Key.from_path(u'Login', 32001L, _app=u'nupter-cn')]
            #self.response.out.write( key )
            
            # queryLogin is a 'GqlQuery' object, has no attribute 'ancestor'
            #entity = queryLogin.ancestor(key)
            
            # 'GqlQuery' object has no attribute 'key'
            #key = queryLogin.key()
            
            # query by KEY in Contact Table
            #queryContact = db.GqlQuery("SELECT * FROM Login WHERE nid = :1", key )
            # note: 不要写错表名
            queryContact = db.GqlQuery("SELECT * FROM Contact WHERE nid = :1", key )
            contacts = queryContact
            
            """
            contacts_query = Contact.all()
            # need to query the use of fetch()?
            contacts = contacts_query.fetch(10)
            """
            
            template_values = { 'contacts': contacts }
            path = os.path.join(os.path.dirname(__file__), 'templates/contact.html')
            # this charset is in HTTP Header
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )

# display Sms
class SmsPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            email = user.email()
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # 最多从数据存储区中抓取1个结果
            key = queryLogin.get()
            
            querySms = db.GqlQuery("SELECT * FROM Sms WHERE nid = :1", key )
            Sms = querySms
            
            template_values = { 'Sms': Sms }
            path = os.path.join( os.path.dirname(__file__), 'templates/sms.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )
 
# display call log 
class CallLogPage(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            email = user.email()
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # 最多从数据存储区中抓取1个结果
            key = queryLogin.get()
            
            queryCallLog = db.GqlQuery("SELECT * FROM CallLog WHERE nid = :1", key )
            calllogs = queryCallLog
            
            template_values = { 'calllogs': calllogs }
            path = os.path.join( os.path.dirname(__file__), 'templates/calllog.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )

# 往cmd表中写构造好的命令的，用短信猫的方式也要这样做
class CmdAction(webapp.RequestHandler):
    @staticmethod
    def getRequestParams(requestQueryString, paramsList):
        # requestQueryString: [sms=Sms&calllog=Calllog&backup=Backup] at first
        requestQueryString = "&" + requestQueryString       # union
        paramIndexes = [(param, requestQueryString.find('&' + param + '=')) for param in paramsList]
        
        paramIndexes = sorted(  filter(lambda x: x[1]!=-1, paramIndexes), key=lambda x:x[1] )
        
        paramIndexes = [(paramIndexes[i][0], paramIndexes[i][1] + len(paramIndexes[i][0]) + 2, len(requestQueryString) if (i == (len(paramIndexes)-1)) else paramIndexes[i+1][1]) for i in range(len(paramIndexes))]
        
        return dict((param[0], urllib.unquote(requestQueryString[param[1]:param[2]])) for param in paramIndexes)
        
    def post(self):
        # 用post时，得到是value，name并不会得到，name是服务端提取数据的标示符
        strContact = self.request.get('contact')
        strSms = self.request.get('sms')
        strCalllog = self.request.get('calllog')
        # submit按钮也会产生数据？至少get请求是这样的。test: post also!
        strSubmit = self.request.get('backup')
        
        self.response.headers['Content-Type'] = 'text/html; charset=GBK'
        self.response.out.write( strContact )
        self.response.out.write( strSms )
        self.response.out.write( strCalllog )
        self.response.out.write( strSubmit )
    
    def get(self):
    # 即使后面跟着一堆参数，还是能跳转到这里
        user = users.get_current_user()
        
        # if not loginned, let user login first
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            # test for 'CmdHandler'
#            self.response.out.write( int('46001') )     # test: 46001
#            entity = db.Model.get_by_id( int('46001') )
#            self.response.out.write( type(entity) )     # test: 无显示
#            self.response.out.write( entity.key() )     # 'NoneType' object has no attribute 'key'
            
            email = user.email()
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # 最多从数据存储区中抓取1个结果
            key = queryLogin.get()
            # test: 'key' agludXB0ZXItY25yDQsSBUxvZ2luGIH6AQw
            #self.response.out.write(key)
        
            # 得到url，因为每个不同的嘛
            strQuery = self.request.query_string
            
            # 从url中提取出参数, add 'delete', add 'lock' and 'unlock'
            requestParams = CmdAction.getRequestParams(strQuery, ['contact', 'sms', 'calllog', 'backup', 'delete', 'lock', 'unlock'])
            if requestParams.has_key("backup"):
                # test: Success! [Backup]
                #strCmd = requestParams["backup"]
                
                strCmd = 'b'
                if requestParams.has_key("contact"):
                    strCmd += '0'
                if requestParams.has_key("sms"):
                    strCmd += '1'
                if requestParams.has_key("calllog"):
                    strCmd += '2'
                    
                cmd = Cmd()
                cmd.message = strCmd
                #cmd.nid = db.Key(key)  # BadArgumentError: Key() expects a string
                #cmd.nid = db.get(key)  # 'list' object has no attribute 'has_key'
                #cmd.nid = key          # 'list' object has no attribute 'has_key'
                #cmd.nid = db.Key( str(key) ) # BadKeyError: Invalid string key [datastore_types.Key.from_path(u'Login', 32001L, _app=u'nupter-cn')].
                #cmd.nid = db.Key( key.__str__() )  # BadKeyError: Invalid string key
                #cmd.nid = db.get(key).key()    # AttributeError: 'list' object has no attribute 'key'
                cmd.nid = key
                cmd.put()
                    
                # test: Success!
                #self.response.headers['Content-Type'] = 'text/html; charset=GBK'
                #self.response.out.write( strCmd )
                
                # test: [datastore_types.Key.from_path(u'Login', 32001L, _app=u'nupter-cn')]
                #self.response.out.write( key )
                
                # should use Ajax
                #self.redirect('http://nupter-cn.appspot.com/backup')
                
                nID = cmd.key().id()
                strEncode = '--' + strCmd + '--' + str( nID ) + '--'
#                strUrl = 'http://nupter-cn.appspot.com/finish?id=' + str( nID )
                strUrl = '/finish?id=' + str( nID )
                
                template_values = {
                    'strEncode': strEncode,
                    'url': strUrl       # test: Success!
                }
                path = os.path.join( os.path.dirname(__file__), 'templates/cmd.html')
                self.response.headers['Content-Type'] = 'text/html; charset=GBK'
                self.response.out.write( template.render(path, template_values) )
                
            #if requestParams.has_key("delete"):
            elif requestParams.has_key("delete"):
                strCmd = 'd'
                if requestParams.has_key("contact"):
                    strCmd += '0'
                if requestParams.has_key("sms"):
                    strCmd += '1'
                if requestParams.has_key("calllog"):
                    strCmd += '2'
                    
                cmd = Cmd()
                cmd.message = strCmd
                cmd.nid = key
                cmd.put()
                
                #self.redirect('http://nupter-cn.appspot.com/wipe')
                nID = cmd.key().id()
                strEncode = '--' + strCmd + '--' + str( nID ) + '--'
#                strUrl = 'http://nupter-cn.appspot.com/finish?id=' + str( nID )
                strUrl = '/finish?id=' + str( nID )
                
                template_values = {
                    'strEncode': strEncode,
                    'url': strUrl
                }
                path = os.path.join( os.path.dirname(__file__), 'templates/cmd.html')
                self.response.headers['Content-Type'] = 'text/html; charset=GBK'
                self.response.out.write( template.render(path, template_values) )
                
            elif requestParams.has_key("lock"):
                strCmd = 'l0'
                
                cmd = Cmd()
                cmd.message = strCmd
                cmd.nid = key
                cmd.put()
                
                nID = cmd.key().id()
                strEncode = '--' + strCmd + '--' + str( nID ) + '--'
                strUrl = '/finish?id=' + str( nID )
                
                template_values = {
                    'strEncode': strEncode,
                    'url': strUrl
                }
                path = os.path.join( os.path.dirname(__file__), 'templates/cmd.html')
                self.response.headers['Content-Type'] = 'text/html; charset=GBK'
                self.response.out.write( template.render(path, template_values) )
                
            elif requestParams.has_key("unlock"):
                strCmd = 'l1'
                
                cmd = Cmd()
                cmd.message = strCmd
                cmd.nid = key
                cmd.put()
                
                nID = cmd.key().id()
                strEncode = '--' + strCmd + '--' + str( nID ) + '--'
                strUrl = '/finish?id=' + str( nID )
                
                template_values = {
                    'strEncode': strEncode,
                    'url': strUrl
                }
                path = os.path.join( os.path.dirname(__file__), 'templates/cmd.html')
                self.response.headers['Content-Type'] = 'text/html; charset=GBK'
                self.response.out.write( template.render(path, template_values) )
            else:
                self.response.set_status(404)
    
# handling lock and unlock
class LockHandler(webapp.RequestHandler):
    # just for test in web browser
    def get(self):
        self.response.out.write('Just for testing in LockHandler!')
    def post(self):
        # get body of HTTP
        strXML = self.request.body  # it's a XML string
        # parse XML, docXML is a Document Node
        docXML = minidom.parseString(strXML)
        
        phone = Phone()
        # must add '[0]', or it's a NodeList
        # TEXT_NODE can use 'data'
        #phone.nid = docXML.getElementsByTagName('nid')[0].firstChild.data
        strKEY = docXML.getElementsByTagName('phone')[0].getAttribute('nid')
        phone.nid = db.Key( strKEY )
        phone.num = docXML.getElementsByTagName('num')[0].firstChild.data
        phone.lock = docXML.getElementsByTagName('lock')[0].firstChild.data
        
        """
        phoneNode = docXML.firstChild                           # <phone>
        phone.nid = phoneNode.childNodes[1].nodeValue           # <nid>
        phone.num = phoneNode.childNodes[1].nodeValue           # <num>
        phone.lock = phoneNode.childNodes[2].nodeValue          # <lock>
        """
        # test
        # Element instance has no attribute 'wholeText'
        #phone.nid = phoneNode.childNodes[0].wholeText
        
        # test
        #Element instance has no attribute 'data'
        # 'data' must be used in Node.TEXT_NODE
        #phone.nid = phoneNode.childNodes[0].data        
        
        phone.put()
        
        # store data into datastore
        #lockdb.strXML = strXML
        #lockdb.put()
        
        # also response data to client
        self.response.set_status(201)
        #self.response.headers['Content-Type'] = 'text/xml'
        #self.response.out.write(strXML)

# handling contact backup
class BackUpHandler(webapp.RequestHandler):
    def post(self):
        # get body of HTTP
        strXML = self.request.body  # it's a XML string        
        # parse XML, docXML is a Document Node
        docXML = minidom.parseString(strXML)
        
        # test use 'for'
        nodeList = docXML.getElementsByTagName('entity')
        # 为了提高效率，先把strKEY计算好！
        # 通过将编码为字符串的键传递到 Key 构造函数（encoded 参数），可以将其转换回 Key对象
        key = db.Key( docXML.getElementsByTagName('contact')[0].getAttribute('nid') )
        dataList = []
        for node in nodeList:
            contact = Contact()
            # 但是发现每次都计算一次，效率太低了！
            # String to KEY
            #contact.nid = db.Key( 
            #           docXML.getElementsByTagName('contact')[0].getAttribute('nid')
            #                    )
            contact.nid = key
            # because I don't have [enter]?!
            contact.name = node.firstChild.firstChild.data
            contact.phone = node.lastChild.firstChild.data
            #contact.name = node.childNodes[1].firstChild.data
            #contact.phone = node.childNodes[3].firstChild.data
            
            # because put() is expensive
            #contact.put()
            dataList.append(contact)
            
        # just use once put()
        db.put(dataList)
        
        """
        # test getting first data
        contact.nid = docXML.getElementsByTagName('contact')[0].getAttribute('nid')
        contact.name = docXML.getElementsByTagName('name')[0].firstChild.data
        contact.phone = docXML.getElementsByTagName('phone')[0].firstChild.data
        # The Model Class's Instance method
        contact.put()
        # or put(models)?
        #db.put(contact)
        """
        
        """
        # test sucess
        another = Contact() # just need constructor again
        another.nid = docXML.getElementsByTagName('contact')[0].getAttribute('nid')
        another.name = docXML.getElementsByTagName('name')[1].firstChild.data
        another.phone = docXML.getElementsByTagName('phone')[1].firstChild.data
        another.put()
        """
        
        """
        # test can put() twice? after testing, no!
        contact.name = docXML.getElementsByTagName('name')[2].firstChild.data
        contact.phone = docXML.getElementsByTagName('phone')[2].firstChild.data
        contact.put()        
        
        contact.name = docXML.getElementsByTagName('name')[1].firstChild.data
        contact.phone = docXML.getElementsByTagName('phone')[1].firstChild.data
        contact.put()
        """
        
        """
        contacts = []
        contacts.extend()
        """
        
        # also response data to client
        self.response.set_status(201)
        
    def get(self):
        self.response.out.write('Sorry, you don\'t have permission to visit BackUpHandler!')
        self.response.set_status(200)

# get CallLog from Android
class CallLogHandler(webapp.RequestHandler):
    def post(self):
        strXML = self.request.body  # it's a XML string
        docXML = minidom.parseString(strXML)
        
        key = db.Key( docXML.getElementsByTagName('calllog')[0].getAttribute('nid') )
        
        nodeList = docXML.getElementsByTagName('entity')
        dataList = []
        for node in nodeList:
            calllog = CallLog()
            
            calllog.nid = key
            calllog.name = node.firstChild.firstChild.data
            calllog.number = node.childNodes[1].firstChild.data
            calllog.type = node.childNodes[2].firstChild.data
            calllog.date = node.childNodes[3].firstChild.data
            calllog.duration = node.lastChild.firstChild.data
            
            dataList.append(calllog)
        db.put(dataList)
        
        # also response data to client
        self.response.set_status(201)
    
# get Sms from Android
class SmsHandler(webapp.RequestHandler):
    def post(self):
        strXML = self.request.body
        docXML = minidom.parseString(strXML)
        
        key = db.Key( docXML.getElementsByTagName('sms')[0].getAttribute('nid') )
        
        nodeList = docXML.getElementsByTagName('entity')
        dataList = []
        for node in nodeList:
            sms = Sms()
            
            sms.nid = key
            sms.name = node.firstChild.firstChild.data
            sms.number = node.childNodes[1].firstChild.data
            sms.date = node.childNodes[2].firstChild.data
            sms.body = node.lastChild.firstChild.data
            
            dataList.append(sms)
        db.put(dataList)
        
        # also response data to client
        self.response.set_status(201)

# communicate with Android, and receieve Login Data, and response special ID
class LoginHandler(webapp.RequestHandler):
    def post(self):
        strEmail = self.request.get('email')
        strPswd = self.request.get('pswd')
        # newly added!
        strSimNum = self.request.get('sim')
        
        logindb = Login()
        logindb.email = strEmail
        logindb.pswd = strPswd
        logindb.sim = strSimNum         # newly added!
        logindb.put()
        
        # 初始化Phone表，否则Lock页面无法进行
        lock = Phone()
        lock.nid = logindb.key()
        lock.num = strSimNum            # 此时当然就是初始的SIM卡号了啊
        lock.lock = 'false'
        lock.put()
        
        """ # 因为重新设计了Login表，所以不再需要下面的语句了
        # newly added!
        lock = Phone()
        # test logindb.key(): agludXB0ZXItY25yDQsSBUxvZ2luGIH6AQw???
        lock.nid = logindb.key()
        lock.num = strSimNum
        # does this have problem???
        lock.lock = 'false'    # default
        lock.put()
        """
        
        """
        # test to see KEY的样子
        #Sucess!
        lockdb = LockDB()
        lockdb.strXML = strKEY
        lockdb.put()
        """
        
        # now, just response with '201'
        # 这个方法跟其他方法的先后顺序？must at first?!
        # maybe by default?
        self.response.set_status(201)
        
        # receive and response a KEY
        strKEY = str( logindb.key() )
        self.response.out.write(strKEY)
        
        
# 客户端到这里来反馈指令的完成
class CmdHandler(webapp.RequestHandler):
    def post(self):
#        strKey = self.request.get('key')          # 标识哪个用户
        strID = self.request.get('ID')            # 标识哪条指令
        
        # 返回的是一个GqlQuery类对象
        # 中间是用AND吗?
        # message怎么可能等于strID呢
        #q = db.GqlQuery('SELECT * FROM Cmd WHERE nid = :1 AND message = :2', strKey, strID)
#        q = db.GqlQuery('SELECT * FROM Cmd WHERE message = :1', strID) # still has problem
#        results = q.fetch(1)
#        db.delete(results)
        
        # 根据entity的ID查到对应的那条记录
        #entity = db.Model.get_by_id( int(strID) )
        entity = Cmd.get_by_id( int(strID) )
        entity.delete()             # db.delete(entity)
        
        # 对于lock和unlock的反馈，还应该
        
        self.response.set_status(201)
        
        """
        # 客户端到这里来获取指令
        # 接收客户端发来的KEY，以字符串的形式
        # 客户端最好是以get方式请求，这样能减少数据的吧？
        
        # 根据KEY，读cmd表中是否有记录，无则直接返回请求的资源不存在的那个码
        self.response.set_status(404)
        
        # 有则从数据库中读取出来，并以表单变量的形式‘cmd’返回，读出一条返回一条
        # 需要看webapp的文档如何返回一个字符串
        
        # 最好是长连接技术，等客户端反馈完了再结束
        
        # 然后删除刚刚发过去的指令(集)
        """
        
# deal with '/finish'
class StateHandler(webapp.RequestHandler):
    def get(self):
        user = users.get_current_user()
        # if not loginned, let user login first
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            # 得到url，因为每个不同的嘛
            strQuery = self.request.query_string
            # 从url中提取出参数
            requestParams = CmdAction.getRequestParams(strQuery, ['id'])
            
            if requestParams.has_key('id'):
                strID = requestParams['id']
                # 最好不在服务端进行循环操作
#                while ( Cmd.get_by_id( int(strID) ) is not None ):
                    # wait 5 seconds，或者客户端JavaScript定时提交请求
                if ( Cmd.get_by_id( int(strID) ) is not None ):
                    self.response.out.write('NO')
                    self.response.set_status(200)
                else:   # cmd has finished
                    
                    self.response.set_status(200)
            else:
                self.response.set_status(404)

# test handling xml data in Windows Mobile
# Sucess!
class TestHandler(webapp.RequestHandler):
    def post(self):
        strXML = self.request.body  # it's a XML string
        
        lockdb = LockDB()
        lockdb.strXML = strXML
        lockdb.put()
        
        self.response.set_status(201)
    
def main():
    application = webapp.WSGIApplication([
                                        ('/', MainPage),
                                        ('/lock', LockPage),
                                        ('/backup', BackupPage),
                                        ('/wipe', WipePage),
                                        ('/contact', ContactPage),
                                        ('/sms', SmsPage),
                                        ('/calllog', CallLogPage),
                                        ('/cmd.do', CmdAction),
                                        ('/finish', StateHandler),      # 状态查询的
                                        ('/rpc/lock', LockHandler),
                                        ('/rpc/backup', BackUpHandler),
                                        ('/rpc/calllog', CallLogHandler),
                                        ('/rpc/sms', SmsHandler),
                                        ('/rpc/test', TestHandler),
                                        ('/rpc/cmd', CmdHandler),       # 远程命令
                                        ('/rpc/login', LoginHandler),   # need ","?
                                        ],
                                       debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()