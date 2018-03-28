#_author_ : duany_000
#_date_ : 2018/3/23
from repository.BaseAdmin import BaseAdmin

class AdminSite(object):
    def __init__(self):
        self.enabled_admins = {}  # model_class class -> admin_class instance

    def register(self,model_class,admin_class=None):
        # print("register>>>",model_class,admin_class)
        app_name = model_class._meta.app_label
        model_name = model_class._meta.model_name
        # print("app_name, model_name>>>",app_name, model_name)
        # admin_class.model = model_name  # 定义model
        if not admin_class:  #为了避免多个model共享同一个BaseKingAdmin内存对象
            admin_class = BaseAdmin()
        else:
            admin_class = admin_class()
        admin_class.model = model_class   #把model_class赋值给了admin_class
        if app_name not in self.enabled_admins:
            self.enabled_admins[app_name] = {}
        self.enabled_admins[app_name][model_name] = admin_class
        # print('adminSite>>',self.enabled_admins)

site = AdminSite()


