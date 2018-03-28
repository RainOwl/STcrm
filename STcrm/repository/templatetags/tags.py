# _author_ : duany_000
# _date_ : 2018/3/24
from django.template import Library
from django.utils.safestring import mark_safe
import datetime, time

register = Library()


@register.simple_tag
def col_data_display(row_obj, admin_class):
    # print(row_obj.name,row_obj.source)
    # print(row_obj, admin_class)
    ele = ""
    if admin_class.list_display:
        for col_index, col_name in enumerate(admin_class.list_display):
            column_obj = admin_class.model._meta.get_field(col_name)
            if column_obj.choices:  # 字段有choice选项
                col_data = getattr(row_obj, 'get_%s_display' % col_name)()
            else:
                col_data = getattr(row_obj, col_name)
            td_ele = "<td>%s</td>" % col_data
            if col_index == 0:
                td_ele = '<td><a href="%s/change">%s</a></td>' % (row_obj.id, col_data)
            ele += td_ele
    else:
        td_ele = "<td>%s</td>" % row_obj  # 直接调用__str__方法
        ele += td_ele
    return mark_safe(ele)

# 生成筛选选项
@register.simple_tag
def build_filter_ele(filter_column, admin_class):
    checked_col = False
    for filter_col in admin_class.filter_conditions:  # 判断是否为已选择条件字段
        filter_col = filter_col.split('__', 1)[0]
        if filter_col == filter_column:
            checked_col = True

    column_obj = admin_class.model._meta.get_field(filter_column)
    # print("column obj,filter_column>>>",filter_column, column_obj)

    # 获取url,拼接args
    # url_str = combined_url_args(admin_class)

    try:
        filter_ele = "<select name='%s'>" % filter_column
        # print(column_obj.get_choices())  # [('', '---------'), (0, '未报名'), (1, '已报名'), (2, '已退学')]
        for choice_item in column_obj.get_choices():
            # print("choice_item>>>",choice_item)
            if checked_col and str(choice_item[0]) == admin_class.filter_conditions[filter_column]:
                tag_opt = '<option value="%s" selected>%s</option>' % (choice_item[0], choice_item[1])
            else:
                tag_opt = '<option value="%s">%s</option>' % (choice_item[0], choice_item[1])

            filter_ele += tag_opt
    except AttributeError as e:
        if column_obj.get_internal_type() in ('DateField', 'DateTimeField'):
            filter_ele = "<select name='%s__gte'>" % filter_column
            now_datetime = datetime.datetime.now()
            time_list = [
                ['', '------'],
                [now_datetime, 'Today'],
                [now_datetime - datetime.timedelta(7), '七天内'],
                [now_datetime.replace(day=1), '本月'],
                [now_datetime - datetime.timedelta(90), '三个月内'],
                [now_datetime.replace(month=1, day=1), '今年内'],
                ['', 'ALL'],
            ]

            for time_opt in time_list:
                opt_val = '' if not time_opt[0] else '%s-%s-%s' % (
                time_opt[0].year, time_opt[0].month, time_opt[0].day)  # 格式化时间
                # print("opt_val>>",opt_val)
                if checked_col and opt_val == admin_class.filter_conditions['%s__gte' % filter_column]:
                    tag_opt = '<option value="%s" selected>%s</option>' % (opt_val, time_opt[1])
                else:
                    tag_opt = '<option value="%s">%s</option>' % (opt_val, time_opt[1])

                filter_ele += tag_opt

    filter_ele += '</select>'
    return mark_safe(filter_ele)


@register.simple_tag
def get_model_name(admin_class):
    return admin_class.model._meta.model_name.upper()

# 生成分页
@register.simple_tag
def render_paginator(querysets, admin_class):
    url_str = combined_url_args(admin_class, '_page')

    ele = """<ul class="pagination">"""
    hidden = ''
    if querysets.number == 1: # 当前页是首页
        hidden = 'display: none;'
    pre_page_li = '<li style="%s"><a href="?_page=%s%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>'%(hidden, querysets.number-1,url_str)
    ele += pre_page_li
    for p_item in querysets.paginator.page_range:
        active = ''
        if abs(p_item - querysets.number) < 2:  # querysets.number当前页
            if p_item == querysets.number:
                active = 'active'
            tag_li = '<li class="%s"><a href="?_page=%s%s">%s</a></li>' % (active, p_item, url_str, p_item)
            ele += tag_li

    if querysets.number == querysets.paginator.num_pages:  # 当前页是尾页
        hidden = 'display: none;'
    else:
        hidden = ''
    next_page_li = '<li style="%s"><a href="?_page=%s%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>'%(hidden,querysets.number+1,url_str)
    ele += next_page_li

    ele += '</ul>'
    return mark_safe(ele)


@register.filter
def sorted_list_display(list_display):
    return enumerate(list_display)

# 生成排序字段
@register.simple_tag
def get_sorted_column(col_index, admin_class, sort_col_index):  # sort_col_index of type_str
    col_index = str(col_index)
    if sort_col_index:
        if sort_col_index.startswith('-'):
            col_index = col_index.strip('-')
        else:
            col_index = '-%s' % col_index
        return col_index
    else:
        col_index = '-%s' % col_index
        return col_index

# 排序字段箭头符号
@register.simple_tag
def render_sorted_arrow(col_index, sort_col_index):
    # print("sort_col_index>>",col_index,sort_col_index)
    if sort_col_index and col_index == abs(int(sort_col_index)):
        if sort_col_index.startswith('-'):
            arrow_direction = 'bottom'
        else:
            arrow_direction = 'top'
        ele = '''<span class="glyphicon glyphicon-triangle-%s" aria-hidden="true"></span>''' % arrow_direction
        return mark_safe(ele)
    return ''


# 拼接参数字段
@register.simple_tag
def combined_url_args(admin_class,deal_arg):
    extra_args = ['_page','_o']
    if deal_arg == '_o':  # 处理排序
        extra_args = ['_page','_o']
    elif deal_arg == '_page':  # 处理分页
        extra_args = ['_page',]
    if admin_class.url_args:
        url_str = ''
        for k,v in admin_class.url_args.items():
            if k not in extra_args:
                url_str += '&%s=%s' %(k,v)

        return mark_safe(url_str)
    return ''

@register.simple_tag
def combined_url_o(admin_class):
    return admin_class.url_args['_o']

@register.simple_tag
def get_obj_field_val(admin_class, form_obj, field):
    '''返回model obj具体字段的值'''
    # print("field>>",field)
    field_obj = admin_class.model._meta.get_field(field)
    if field_obj.choices:  # 字段有choice选项
       return getattr(form_obj.instance, 'get_%s_display' % field)()
    else:
       return getattr(form_obj.instance, field)
    # return getattr(form_obj.instance, field)



@register.simple_tag
def get_available_m2m_data(admin_class, form_obj, form_item_name):
    """返回的是m2m字段关联表的所有数据"""
    fileds_obj = admin_class.model._meta.get_field(form_item_name)
    obj_list = set(fileds_obj.related_model.objects.all())

    selected_list = set(getattr(form_obj.instance, form_item_name).all())

    return obj_list - selected_list

@register.simple_tag
def get_selected_m2m_data(form_obj, form_item_name):
    """返回已选的m2m数据"""
    selected_list = getattr(form_obj.instance, form_item_name).all()
    return selected_list

@register.simple_tag
def display_all_related_objs(obj):
    """显示要被删除对象的所有关联对象"""
    ele = '<ul>'
    for related_field in obj._meta.related_objects:
        print(related_field)
        related_table_name = related_field.name  # related_field=<ManyToManyRel: repository.customerinfo>
        ele += '<li>%s<ul>'% related_table_name
        related_lookup_key = "%s_set" % related_table_name
        related_objs = getattr(obj, related_lookup_key).all()  # 反向查所有关联的数据
        print(related_objs)

        if related_field.get_internal_type() == "ManyToManyField":  # m2m不需要深入查找
            for i in related_objs:
                ele += "<li><a href='/myadmin/%s/%s/%s/change/'>%s</a> 记录里与[%s]相关的的数据将被删除</li>" \
                       % (i._meta.app_label, i._meta.model_name, i.id, i, obj)
        else:
            for i in related_objs:
                ele += "<li><a href='/myadmin/%s/%s/%s/change/'>%s</a></li>" % (i._meta.app_label,
                                                                                  i._meta.model_name,
                                                                                  i.id, i)
                ele += display_all_related_objs(i)
        ele += "</ul></li>"
    ele += "</ul>"
    return ele

