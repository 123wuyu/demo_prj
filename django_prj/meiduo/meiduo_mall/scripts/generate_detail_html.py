
# 添加导包路径 : /home/python/code/gz07/meiduo/meiduo_mall
import sys
# sys.path.append('../')  # 表示把 scripts 目录的上一级目录 添加到导包路径中
sys.path.insert(0, '../')
print(sys.path)

# 加载django配置文件, 注册应用
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "meiduo_mall.settings.dev")
django.setup()


from celery_tasks.html.tasks import generate_static_sku_detail_html
from goods.models import SKU


if __name__ == '__main__':
    """批量生成所有商品的静态详情页"""
    skus = SKU.objects.all()
    for sku in skus:
        sku_id = sku.id
        generate_static_sku_detail_html(sku_id)   #  生成一个商品的静态详情页
        print(sku_id)


