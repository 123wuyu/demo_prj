import xadmin
from xadmin import views

from goods import models


class BaseSetting(object):
    """xadmin的基本配置"""
    enable_themes = True        # 开启主题切换功能
    # use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "美多商城运营管理系统"   # 设置站点标题
    site_footer = "美多商城集团有限公司"  # 设置站点的页脚
    menu_style = "accordion"            # 设置菜单折叠


# Common
xadmin.site.register(views.CommAdminView, GlobalSettings)


class SKUAdmin(object):

    model_icon = 'fa fa-comment-o'
    list_display = ['id', 'name', 'price', 'stock', 'sales', 'comments']
    search_fields = ['id', 'name']
    list_filter = ['category']
    list_editable = ['price', 'stock']
    show_bookmarks = True               # 添加书签
    show_detail_fields = ['name']

    def save_models(self):
        # 新增或修改sku对象, 会执行此方法
        pass

    def delete_model(self):
        # 删除一条数据, , 会执行此方法
        pass


xadmin.site.register(models.SKU, SKUAdmin)

xadmin.site.register(models.GoodsCategory)
xadmin.site.register(models.GoodsChannel)
xadmin.site.register(models.Goods)
xadmin.site.register(models.Brand)
xadmin.site.register(models.GoodsSpecification)
xadmin.site.register(models.SpecificationOption)
xadmin.site.register(models.SKUSpecification)
xadmin.site.register(models.SKUImage)


