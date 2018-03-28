#_author_ : duany_000
#_date_ : 2018/3/24

class BaseAdmin(object):
    list_display = []
    list_filter = []
    search_fields = []
    readonly_fields = []
    filter_horizontal = []
    list_per_page = 10