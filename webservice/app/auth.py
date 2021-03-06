from tornado.web import RequestHandler
from config import Config
import uuid

def auth(fun):
    def auth_wrap(obj, *args, **kwargs):
        if not obj.get_cookie('token_id'):
            return obj.redirect('/')
        fun(obj, *args, **kwargs)
    return auth_wrap

class AuthHandler(RequestHandler):
    '''认证'''
    conf = Config()
    def check_user_passwd(self, user="admin", passwd=""):
        try:
            default_user = self.conf.auth['username']
            default_passwd = self.conf.auth['passwd']
            if user == default_user and passwd == default_passwd:
                return True
            else:
                return False
        except Exception as e:
            print(e)

    def post(self, method):
        ret = {}
        if method == "update":
            old_passwd = self.get_argument('opwd')
            flag = self.check_user_passwd(passwd=old_passwd)
            if flag:
                ret['status'] = 'success'
                self.conf.auth['passwd'] = self.get_argument('pwd1')
                self.conf.save()
                self.clear_cookie("token_id")
            else:
                ret['status'] = 'failed'
                ret['err_msg'] = "原始密码错误"
        elif method == "login":
            flag = self.check_user_passwd(self.get_argument('user'), self.get_argument('pass'))
            if (flag):
                ret['status'] = 'success'
            else:
                ret['status'] = 'failed'
            self.set_cookie('token_id', str(uuid.uuid4()))
        self.write(ret)
        # print(self.get_arguments('pass'))

    @auth
    def get(self):
        self.render("password.html")

class LoginHandler(RequestHandler):
    # @auth
    def get(self):
        if self.get_cookie('token_id'):
            self.redirect('/setup')
        else:
            self.render("login.html")