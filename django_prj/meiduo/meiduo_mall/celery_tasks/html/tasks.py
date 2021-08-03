# html/tasks.py
from celery_tasks.main import celery_app
from django.template import loader
from django.conf import settings
import os

from contents.crons import get_categories
from goods.models import SKU


@celery_app.task(name='generate_static_list_search_html')
def generate_static_list_search_html():
    """
    生成静态的商品列表页和搜索结果页html文件
    """
    # 商品分类菜单
    categories = get_categories()

    # 渲染模板，生成静态html文件
    context = {
        'categories': categories,
    }

    template = loader.get_template('list.html')
    html_text = template.render(context)  # 生成半静态化的list.html

    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'list.html')
    with open(file_path, 'w') as f:
        f.write(html_text)


@celery_app.task(name='generate_static_sku_detail_html')
def generate_static_sku_detail_html(sku_id):
    """
    生成静态商品详情页面
    :param sku_id: 商品sku id
    """
    # 商品分类菜单
    categories = get_categories()

    # 获取当前sku的信息
    sku = SKU.objects.get(id=sku_id)
    sku.images = sku.skuimage_set.all()

    # 面包屑导航信息中的频道
    goods = sku.goods
    # 根据 商品类别 查询所属的频道
    goods.channel = goods.category1.goodschannel_set.all()[0]

    # 构建当前商品的规格键
    # sku_key = [规格1参数id， 规格2参数id， 规格3参数id, ...]
    sku_specs = sku.skuspecification_set.order_by('spec_id')
    sku_key = []
    for spec in sku_specs:
        sku_key.append(spec.option.id)

    # 获取当前商品的所有SKU
    skus = goods.sku_set.all()

    # 构建不同规格参数（选项）的sku字典
    # spec_sku_map = {
    #     (规格1参数id, 规格2参数id, 规格3参数id, ...): sku_id,
    #     (规格1参数id, 规格2参数id, 规格3参数id, ...): sku_id,
    #     ...
    # }
    spec_sku_map = {}
    for s in skus:
        # 获取sku的规格参数
        s_specs = s.skuspecification_set.order_by('spec_id')
        # 用于形成规格参数sku字典的键
        key = []
        for spec in s_specs:
            key.append(spec.option.id)
        # 向规格参数sku字典添加记录
        spec_sku_map[tuple(key)] = s.id

    # 获取当前商品的规格信息: sku_id = 1  macbook电脑
    # specs = [
    #    {
    #        'name': '屏幕尺寸',
    #        'options': [
    #            {'value': '13.3寸', 'sku_id': 1 },
    #            {'value': '15.4寸', 'sku_id': 2 },
    #        ]
    #    },
    #    {
    #        'name': '颜色',
    #        'options': [
    #            {'value': '银色', 'sku_id': 1 },
    #            {'value': '黑色', 'sku_id': None }
    #        ]
    #    },
    #    {
    #        'name': '版本',
    #        'options': [
    #            {'value': '256G存储', 'sku_id': None },
    #            {'value': '128G存储', 'sku_id': None },
    #            {'value': '512G存储', 'sku_id': 1 }
    #        ]
    #    },
    # ]
    specs = goods.goodsspecification_set.order_by('id')

    # 若当前sku的规格信息不完整，则不再继续
    if len(sku_key) < len(specs):
        return

    for index, spec in enumerate(specs):
        # 复制当前sku的规格信息 （复制列表中的所有元素，得到一个新的列表, ：表示切片操作）
        key = sku_key[:]
        # 该规格的选项
        options = spec.specificationoption_set.all()
        for option in options:
            # 在规格参数sku字典中查找符合当前规格的sku
            key[index] = option.id
            option.sku_id = spec_sku_map.get(tuple(key))

        spec.options = options

    # 渲染模板，生成静态html文件
    context = {
        'categories': categories,  # 商品频道和类别数据
        'goods': goods,     # 当前商品所属的spu
        'specs': specs,     # 当前商品的规格信息
        'sku': sku          # 当前商品详情信息
    }

    template = loader.get_template('detail.html')
    html_text = template.render(context)
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR,
                             'goods/' + str(sku_id) + '.html')
    with open(file_path, 'w') as f:
        f.write(html_text)