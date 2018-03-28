from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import json

from myadmin.admin_regist_dict import global_dict
from myadmin.sites import site
from repository import models
from myadmin import form_handle


# Create your views here.


def acc_login(request):
    if request.method == 'GET':
        return render(request, 'myadmin/acc_login.html')

    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = authenticate(request, username=username, password=password)
        if user_obj:
            login(request, user_obj)
            return redirect(request.GET.get('next', '/myadmin/'))
            # return redirect('/sale/')
        else:
            error_msg = 'Wrong username or password!'
            return render(request, 'myadmin/acc_login.html', {'error_msg': error_msg})


def acc_logout(request):
    logout(request)
    return redirect('/myadmin/login/')


@login_required
@global_dict
def app_index(request):
    print("sites.", site.enabled_admins)
    pro_model_admin = site.enabled_admins
    # print(pro_model_admin)
    return render(request, 'myadmin/app_index.html', {'pro_model_admin': pro_model_admin, })


@login_required
@global_dict
def table_detail(request, app_name, model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    # model_class = admin_class.model
    # print("admin_class,model_class>>>",admin_class,model_class)

    # 根据筛选条件得到数据集
    querysets, filter_conditions = get_filter_result(request, admin_class)
    print("filter_conditions>>",filter_conditions)  #  {'source': '2'}
    admin_class.filter_conditions = filter_conditions
    admin_class.url_args = filter_conditions

    # search条件处理
    querysets,search_val = get_serached_result(request,querysets,admin_class)
    admin_class.search_val = search_val
    if search_val:
        admin_class.url_args['_q'] = search_val

    # 排序处理
    querysets, sort_col_index = get_orderby_result(request, querysets, admin_class)
    admin_class.url_args['_o'] = sort_col_index

    # 处理页码
    paginator = Paginator(querysets, admin_class.list_per_page)  # Show 2 contacts per page
    page = request.GET.get('_page')
    print('page>>',page)
    if page:
        admin_class.url_args['_page'] = page
    try:
        querysets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        querysets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        querysets = paginator.page(paginator.num_pages)

    print("url_args>>>",admin_class.url_args)
    return render(request, 'myadmin/table_detail.html',
                  {'querysets': querysets,
                    'admin_class': admin_class,
                    'sort_col_index':sort_col_index if sort_col_index else ''})

# 筛选结果
def get_filter_result(request, admin_class):
    filter_conditions = {}
    for filter_col, filter_data in request.GET.items():
        if filter_col in ('_page','_o','_q'):continue
        if filter_data:
            filter_conditions[filter_col] = filter_data

    filter_querysets = admin_class.model.objects.filter(**filter_conditions).order_by('-id')
    return filter_querysets, filter_conditions

# 排序结果
def get_orderby_result(request, querysets, admin_class):
    sort_col_index = request.GET.get('_o')
    if sort_col_index:
        orderby_key = admin_class.list_display[abs(int(sort_col_index))]

        if sort_col_index.startswith('-'):
            orderby_key =  '-'+ orderby_key
        return querysets.order_by(orderby_key), sort_col_index
    else:
        return querysets,''

#search结果
def get_serached_result(request,querysets,admin_class):
    search_val = request.GET.get('_q')
    if search_val:
        q = Q()
        q.connector = 'OR'

        for search_field in admin_class.search_fields:
            q.children.append(("%s__contains" % search_field, search_val))

        return querysets.filter(q),search_val
    return querysets,search_val

###########update############

@login_required
@global_dict
def table_obj_change(request,app_name,model_name,row_id):
    admin_class = site.enabled_admins[app_name][model_name]
    update_item = admin_class.model.objects.get(id=row_id)
    model_form = form_handle.create_dynamic_model_form(admin_class)

    if request.method == 'GET':
        form_obj = model_form(instance=update_item)
    elif request.method == 'POST':
        form_obj = model_form(instance=update_item, data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s'% (app_name, model_name))
    return render(request, 'myadmin/table_obj_chage.html',locals())

###########add############
@login_required
@global_dict
def table_obj_add(request,app_name,model_name):
    admin_class = site.enabled_admins[app_name][model_name]
    model_form = form_handle.create_dynamic_model_form(admin_class,True)
    if request.method == 'GET':
        form_obj = model_form()
    elif request.method == 'POST':
        form_obj = model_form(data=request.POST)
        if form_obj.is_valid():
            form_obj.save()
            return redirect('/myadmin/%s/%s'% (app_name, model_name))
    return render(request, 'myadmin/table_obj_add.html',locals())

##############delete##############
@login_required
@global_dict
def table_obj_delete(request,app_name,model_name,row_id):
    admin_class = site.enabled_admins[app_name][model_name]
    obj = admin_class.model.objects.get(id=row_id)

    if request.method == 'POST':
        obj.delete()
        return redirect("/myadmin/{app_name}/{model_name}/".format(app_name=app_name,model_name=model_name))
    return render(request, 'myadmin/table_obj_delete.html', locals())



