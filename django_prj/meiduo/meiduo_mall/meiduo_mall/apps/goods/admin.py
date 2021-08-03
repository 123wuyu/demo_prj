from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

from celery_tasks.html.tasks import generate_static_list_search_html, generate_static_sku_detail_html
from goods import models


class SKUAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        # 修改或新增了商品，需要重新生成详情页
        obj.save()  # obj  商品sku对象

        generate_static_sku_detail_html(obj.id)  # 重新生成商品详情页
        # generate_static_sku_detail_html.delay(obj.id)


class SKUSpecificationAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """商品选项信息的修改"""
        obj.save()

        generate_static_sku_detail_html(obj.sku.id)     # 重新生成商品详情页
        # generate_static_sku_detail_html.delay(obj.sku.id)

    def delete_model(self, request, obj):
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html(sku_id)


class SKUImageAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        """新增商品图片"""
        obj.save()   # SKUImage 类型的对象
        generate_static_sku_detail_html(obj.sku.id)    # 重新生成商品详情页

        # 判断商品是否有默认图片，如果没有， 则在新增商品图片时进行设置
        sku = obj.sku
        if not sku.default_image_url:  # 默认图片为空
            sku.default_image_url = obj.image.url  # 设置商品默认图片
            sku.save()

    def delete_model(self, request, obj):
        """删除商品图片"""
        sku_id = obj.sku.id
        obj.delete()
        generate_static_sku_detail_html(sku_id)   # 重新生成商品详情页


class GoodsCategoryAdmin(ModelAdmin):

    def save_model(self, request, obj, form, change):
        """admin后台新增或修改了数据时调用"""
        obj.save()  # 新增或修改数据

        generate_static_list_search_html()        # 重新生成半静态化的列表页
        # generate_static_list_search_html.delay()    # 重新生成半静态化的列表页

    # def save_model(self, request, obj, form, change):
    #     super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        """admin后台删除了数据时调用"""
        obj.delete()
        generate_static_list_search_html()    # 重新生成半静态化的列表页
        # generate_static_list_search_html.delay()  # 重新生成半静态化的列表页


admin.site.register(models.GoodsCategory, GoodsCategoryAdmin)
admin.site.register(models.GoodsChannel)
admin.site.register(models.Brand)
admin.site.register(models.Goods)
admin.site.register(models.GoodsSpecification)
admin.site.register(models.SpecificationOption)

# admin.site.register(models.SKU)
# admin.site.register(models.SKUImage)
# admin.site.register(models.SKUSpecification)

admin.site.register(models.SKU, SKUAdmin)
admin.site.register(models.SKUSpecification, SKUSpecificationAdmin)
admin.site.register(models.SKUImage, SKUImageAdmin)
