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
#   2010-03-18: ��������ʱӦ�ü���Ѿ����ڣ�����BackUpHandler��(�Ȳ�����)
#               login in different mobile, create LoginHandler
#               test in Windows Mobile, create TestHandler
#               main finish LoginHandler
#   2010-03-19: �ٴ��޸����ݱ����ƣ�ʹ��References
#               response with a KEY in LoginHandler
#               ����KEY, �޸�BackupHandler�Ļ���
#               ������HTMLǰ̨ҳ��Ŀ�ܣ��������ٰ���������
#               �����KEY��ContactPage���������ˣ�neet to add some functions
#   2010-03-20: solve ['unicode' object has no attribute 'has_key'] in ContactPage
#               according KEY, read specifical contacts out in ContactPage
#   2010-03-22: 1. solve [AttributeError: 'NoneType' object has no attribute 'email']
#               in ContactPage, ���ǲ���½��״̬��ֱ�ӷ���/contact�����
#               ����Ϊʲô��Lockҳ��������ת����?
#               2. ���´����������֮��Ĺ�ϵ�������δ��¼��״̬���ʣ�����ת��google
#               in all pages, add [self.redirect(url)]
#               3. write BackupPage
#               4. newly add WipePage, SmsPage, CallLogPage
#               5. modify MainPage and index.html
#               6. spend a lot of time modifing CSS with WangQin
#               7. add form in backup.html, and newly add BackupAction
#               ���Ĵ����ǲ���ᰡ��
#               8. add class CmdHandler and class Cmd(db.Model)
#   2010-03-23: 1. handle form in BackupAction by post
#               �޸�����д�ı��е�value���������Ҫ����ȥ�ģ���ô����Ӣ����
#               post�����ύ��ȥ��������ʾ�ɹ�
#               2. handle form in BackupAction by get
#               use Google Code Search's [getRequestParams]
#   2010-03-24: 1. add datastore operator in BackupAction
#               have problem in KEY
#               2. modify wipe.html's form
#               3. rename 'BackupAction' to 'CmdAction'
#               4. modify 'MainPage': δ��¼��״̬�·�����ҳ�������ӵ�if user������
#               5. backupҳ�治��ת��wipeҳ����ת, python�е�switch-case���д
#               6. modify lock.html and simply LockPage
#   2010-03-27: 1. newly add 'CallLogHandler', newly add 'CallLog'
#               basic achieve 'CallLogHandler'
#               2. modify 'CallLogPage' and calllog.html
#               3. newly add 'SmsHandler', newly add 'Sms' datastore
#               4. modify 'SmsPage' and sms.html
#   2010-04-05: 1. ������cmd.html
#               2. ��CmdAction�����������ǰ̨��ʾ
#   2010-04-06: 1. modify 'CmdHandler': �ͻ��˵�����������ָ������
#   2010-04-08: 1. add class 'StateHandler'
#   2010-04-09: 1. '/action/cmd.do'��Ϊ'/cmd.do'
#   2010-04-10: 1. ����ˣ���ͨѶ¼Ϊ��ʱ��/contact�������⣡
#               2. modify class LoginHandler to get 'sim'
#   2010-04-11: 1. index.html���ӵ�ǰSIM���ŵ���ʾ����class MainPage��
#               2. �������class Login������ע��ʱ���ֻ��ţ�
#               3. modify class CmdAction�����Ӷ�lockָ��Ĵ���
#               4. modify all html's title 'xx - MobileSecure'
#               5. ��Phone��������time���ԣ���������unlock��ָ�������ֻ��ɾ��cmd�еļ�¼�ˣ�����ȥ����Phone���еļ�¼�ˣ�
#               6. class LoginHandler�г�ʼ��Phone��
#               7. ��class LockPage��ʹ��Query�ӿڣ�����ʹ��GqlQuery
#               8. ������Ҫ��������
#   2010-04-30: 1. �޸�app.yaml������secure�������������ǲ�Ӧ������ʹ�������������Ϊ������Ӹ�����
#
#   Todo:
#   2. ��Դ�����ڵ��Ǹ�����404��
#   done! 3. �����μ�ȫ���Ű��������ܲ����Է��ŵķ�ʽ���������è�ķ�ʽ
#   4. һ�в�������η���д��
#   5. �����ٺ���һ���Ajax
#   must! 6. ��ҳ��IE8.0����ʾ����������
#   7. CmdAction�б������ύ����404
#   done! 8. backupҳ��Ӧ��Ҫ��wipeҳ�������Щ���û���̫�÷ֱ������ĸ�ҳ���°�
#   9. �������޸�lock.html, ������w3school
#   done! 10. �����٣�ͼƬ�����쵽��ô�󣬲�Ҫ�ظ�
#   11. ����˸��ֲ�����Ӧ����https
#   done! 12. why '/sms' will have two [> >]?
#   must! 13. ͨѶ¼һ�࣬http://nupter-cn.appspot.com/contact�ͳ��������ˣ�˵��ģ��������
#   14. http://code.google.com/appengine/docs/python/datastore/keysandentitygroups.html�е�class="prettyprint"�������ǵ�ǰָ̨����ʾ��
#   need! 15. û�����ֻ��ͻ���ע����û��������ǲ��ܵ�½ϵͳ�ģ���Ϊ�����ҷ�ָ�����Login������û�и��û������ݵġ�
#   done! 16. ��ͨѶ¼Ϊ��ʱ��/contact�������⣡
#   17. index.html����ʾSIM����ʱ����ʽ��
#   18. ���׺�ʱ����Ҫ��<div>
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
class Total(db.Model):              # �ܱ���Ӧ��ÿ���ͻ��ˣ����е���Ϣ���ܻ��ܵ���
    email = db.StringProperty()
    pswd = db.StringProperty()
    contact = db.ReferenceProperty(Contact)         # ���ֻ������е�ͨѶ¼
    lock = db.ReferenceProperty(Phone)              # current SIM and locking state
"""

class Login(db.Model):
    # maybe don't need it, because has a key in default
    #nid = db.StringProperty()
    email = db.StringProperty()
    pswd = db.StringProperty()
    sim = db.StringProperty()       # �û�ע��ʱ���ֻ���

class Phone(db.Model):              # lock table and current SIM
    # if I can use data type, better writing is:
    #nid = db.IntegerProperty()
    #num = db.IntegerProperty()
    #lock = db.BooleanProperty()
    
    #pswd = db.StringProperty()
    #location = db.StringProperty()
    
    # need to modify������Ҫ�ѱ�ɾ���ˣ���Ϊ�����Ѿ���������
    nid = db.ReferenceProperty(Login)           # KEY Properties
    #nid = db.StringProperty()
    num = db.StringProperty()                   # ��ǰSIM���ţ�����һ����ԭʼ�İ�
    lock = db.StringProperty()                  # �Ƿ�����
    date = db.DateTimeProperty(auto_now_add=True)   # �ϴ�������¼ʱ��ʱ��

class Contact(db.Model):                        # backup table
    nid = db.ReferenceProperty(Login)           # KEY Properties
    name = db.StringProperty()                  # every contact's name
    # the same name doesn't matter in Python?
    phone = db.StringProperty()                 # every contact's phone
    
class CallLog(db.Model):
    nid = db.ReferenceProperty(Login)           # KEY Properties
    name = db.StringProperty()                  # person called
    number = db.StringProperty()
    type = db.StringProperty()                  # �����л��Ǳ���
    date = db.StringProperty()
    duration = db.StringProperty()              # ͨ������ʱ��
    
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
    message = db.StringProperty()               # ����������ַ���
    nid = db.ReferenceProperty(Login)           # KEY Properties, Ӧ������һ��Entity

# just for test    
class LockDB(db.Model):
    strXML = db.StringProperty(multiline=True)

class MainPage(webapp.RequestHandler):
    def get(self):
        # or use 'users.GetCurrentUser()'?
        user = users.get_current_user()
        
        if user:
            # ��д���ж����ǰ�棬��Ϊ��Ч�����⣬Ҳ��Ҫ�����
            username = user.nickname()
            url = users.create_logout_url(self.request.uri)
            
            email = user.email()
            queryLogin = db.GqlQuery("SELECT * FROM Login WHERE email = :1", email )
            
            entity = queryLogin.get()
            #entity = queryLogin.fetch(1)
            #entitys = queryLogin     # �϶�ֻ��һ����
            
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
                # ����python�﷨��˵����Ȼ������.py file���
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
            
            ''' # ����Query�ӿڣ�����������ô���ڣ�GqlQuery����֧�ֵģ�
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
        #self.response.out.write("test ����")
        
        user = users.get_current_user()
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            template_values = { }
            path = os.path.join( os.path.dirname(__file__), 'templates/backup.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            # ws��ʹ���˸��յ�ģ��ֵ��Ӧ���и��õİ취��
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
        
        # �������else,�����������ȥ�������û�������Ч����yes
        else:
            # ���ǵ�һ�δ���entityʱ������ٻ�ȡ����KEY��
            # according to the Email, we get specifical KEY
            
            # 1.get email, test Success!
            email = user.email()
            # 2.query entity by email in Login Table
            # queryLogin must be a 'GqlQuery' object
            # the use of ancestor()?
            #queryLogin = db.GqlQuery("SELECT * FROM Login WHERE email = :1", email)
            
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # �����д��һ���ǿ��Եģ��������ĳ���û���Login���в����ھͻ�error��
            #entity = queryLogin.fetch(1)
            #key = entity        # �������ַ����͵ģ��Ǹ�key path���͵İɣ�
            key = queryLogin.get()
            
            # test 'key' type: [datastore_types.Key.from_path(u'Login', 32001L, _app=u'nupter-cn')]
            #self.response.out.write( key )
            
            # queryLogin is a 'GqlQuery' object, has no attribute 'ancestor'
            #entity = queryLogin.ancestor(key)
            
            # 'GqlQuery' object has no attribute 'key'
            #key = queryLogin.key()
            
            # query by KEY in Contact Table
            #queryContact = db.GqlQuery("SELECT * FROM Login WHERE nid = :1", key )
            # note: ��Ҫд�����
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
            # �������ݴ洢����ץȡ1�����
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
            # �������ݴ洢����ץȡ1�����
            key = queryLogin.get()
            
            queryCallLog = db.GqlQuery("SELECT * FROM CallLog WHERE nid = :1", key )
            calllogs = queryCallLog
            
            template_values = { 'calllogs': calllogs }
            path = os.path.join( os.path.dirname(__file__), 'templates/calllog.html')
            self.response.headers['Content-Type'] = 'text/html; charset=GBK'
            self.response.out.write( template.render(path, template_values) )

# ��cmd����д����õ�����ģ��ö���è�ķ�ʽҲҪ������
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
        # ��postʱ���õ���value��name������õ���name�Ƿ������ȡ���ݵı�ʾ��
        strContact = self.request.get('contact')
        strSms = self.request.get('sms')
        strCalllog = self.request.get('calllog')
        # submit��ťҲ��������ݣ�����get�����������ġ�test: post also!
        strSubmit = self.request.get('backup')
        
        self.response.headers['Content-Type'] = 'text/html; charset=GBK'
        self.response.out.write( strContact )
        self.response.out.write( strSms )
        self.response.out.write( strCalllog )
        self.response.out.write( strSubmit )
    
    def get(self):
    # ��ʹ�������һ�Ѳ�������������ת������
        user = users.get_current_user()
        
        # if not loginned, let user login first
        if not user:
            url = users.create_login_url(self.request.uri)
            self.redirect(url)
        else:
            # test for 'CmdHandler'
#            self.response.out.write( int('46001') )     # test: 46001
#            entity = db.Model.get_by_id( int('46001') )
#            self.response.out.write( type(entity) )     # test: ����ʾ
#            self.response.out.write( entity.key() )     # 'NoneType' object has no attribute 'key'
            
            email = user.email()
            queryLogin = db.GqlQuery("SELECT __key__ FROM Login WHERE email = :1", email)
            # �������ݴ洢����ץȡ1�����
            key = queryLogin.get()
            # test: 'key' agludXB0ZXItY25yDQsSBUxvZ2luGIH6AQw
            #self.response.out.write(key)
        
            # �õ�url����Ϊÿ����ͬ����
            strQuery = self.request.query_string
            
            # ��url����ȡ������, add 'delete', add 'lock' and 'unlock'
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
        # Ϊ�����Ч�ʣ��Ȱ�strKEY����ã�
        # ͨ��������Ϊ�ַ����ļ����ݵ� Key ���캯����encoded �����������Խ���ת���� Key����
        key = db.Key( docXML.getElementsByTagName('contact')[0].getAttribute('nid') )
        dataList = []
        for node in nodeList:
            contact = Contact()
            # ���Ƿ���ÿ�ζ�����һ�Σ�Ч��̫���ˣ�
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
        
        # ��ʼ��Phone������Lockҳ���޷�����
        lock = Phone()
        lock.nid = logindb.key()
        lock.num = strSimNum            # ��ʱ��Ȼ���ǳ�ʼ��SIM�����˰�
        lock.lock = 'false'
        lock.put()
        
        """ # ��Ϊ���������Login�����Բ�����Ҫ����������
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
        # test to see KEY������
        #Sucess!
        lockdb = LockDB()
        lockdb.strXML = strKEY
        lockdb.put()
        """
        
        # now, just response with '201'
        # ��������������������Ⱥ�˳��must at first?!
        # maybe by default?
        self.response.set_status(201)
        
        # receive and response a KEY
        strKEY = str( logindb.key() )
        self.response.out.write(strKEY)
        
        
# �ͻ��˵�����������ָ������
class CmdHandler(webapp.RequestHandler):
    def post(self):
#        strKey = self.request.get('key')          # ��ʶ�ĸ��û�
        strID = self.request.get('ID')            # ��ʶ����ָ��
        
        # ���ص���һ��GqlQuery�����
        # �м�����AND��?
        # message��ô���ܵ���strID��
        #q = db.GqlQuery('SELECT * FROM Cmd WHERE nid = :1 AND message = :2', strKey, strID)
#        q = db.GqlQuery('SELECT * FROM Cmd WHERE message = :1', strID) # still has problem
#        results = q.fetch(1)
#        db.delete(results)
        
        # ����entity��ID�鵽��Ӧ��������¼
        #entity = db.Model.get_by_id( int(strID) )
        entity = Cmd.get_by_id( int(strID) )
        entity.delete()             # db.delete(entity)
        
        # ����lock��unlock�ķ�������Ӧ��
        
        self.response.set_status(201)
        
        """
        # �ͻ��˵���������ȡָ��
        # ���տͻ��˷�����KEY�����ַ�������ʽ
        # �ͻ����������get��ʽ���������ܼ������ݵİɣ�
        
        # ����KEY����cmd�����Ƿ��м�¼������ֱ�ӷ����������Դ�����ڵ��Ǹ���
        self.response.set_status(404)
        
        # ��������ݿ��ж�ȡ���������Ա���������ʽ��cmd�����أ�����һ������һ��
        # ��Ҫ��webapp���ĵ���η���һ���ַ���
        
        # ����ǳ����Ӽ������ȿͻ��˷��������ٽ���
        
        # Ȼ��ɾ���ոշ���ȥ��ָ��(��)
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
            # �õ�url����Ϊÿ����ͬ����
            strQuery = self.request.query_string
            # ��url����ȡ������
            requestParams = CmdAction.getRequestParams(strQuery, ['id'])
            
            if requestParams.has_key('id'):
                strID = requestParams['id']
                # ��ò��ڷ���˽���ѭ������
#                while ( Cmd.get_by_id( int(strID) ) is not None ):
                    # wait 5 seconds�����߿ͻ���JavaScript��ʱ�ύ����
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
                                        ('/finish', StateHandler),      # ״̬��ѯ��
                                        ('/rpc/lock', LockHandler),
                                        ('/rpc/backup', BackUpHandler),
                                        ('/rpc/calllog', CallLogHandler),
                                        ('/rpc/sms', SmsHandler),
                                        ('/rpc/test', TestHandler),
                                        ('/rpc/cmd', CmdHandler),       # Զ������
                                        ('/rpc/login', LoginHandler),   # need ","?
                                        ],
                                       debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()