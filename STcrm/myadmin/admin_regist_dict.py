#_author_ : duany_000
#_date_ : 2018/3/24
from django import conf

def global_dict(func):
    def inner(*args,**kwargs):
        for app in conf.settings.INSTALLED_APPS:
            try:
                mod = __import__('%s.myadmin'%app)
            except Exception as e:
                pass
        ret = func(*args,**kwargs)
        return ret
    return inner

def global_dict1():
    for app in conf.settings.INSTALLED_APPS:
        try:
            mod = __import__('%s.myadmin' % app)
        except Exception as e:
            pass
