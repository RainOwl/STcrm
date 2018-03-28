#_author_ : duany_000
#_date_ : 2018/3/26
from django.forms import ModelForm
from repository import models

# class CustomerForm(ModelForm):
#     class Meta:
#         model = models.CustomerInfo
#         fields = '__all__'
#         fields = ['name','contact']


def create_dynamic_model_form(admin_class,form_add=False):
    """动态的生成modelform"""
    class meta:
        model = admin_class.model
        fields = '__all__'
        if not form_add:
            exclude = admin_class.readonly_fields
            admin_class.form_add = False
        else:
            admin_class.form_add = True

    def __new__(cls, *args, **kwargs):
        print(cls.base_fields)
        for field_name in cls.base_fields:
            filed_obj = cls.base_fields[field_name]
            filed_obj.widget.attrs.update({'class': 'form-control'})
            # if field_name in admin_class.readonly_fields:
            #     filed_obj.widget.attrs.update({'disabled': 'true'})
        return ModelForm.__new__(cls)

    dynamic_form = type("DynamicModelForm", (ModelForm,), {'Meta': meta,'__new__':__new__})
    return dynamic_form


