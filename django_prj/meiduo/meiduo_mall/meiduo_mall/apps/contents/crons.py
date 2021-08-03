import time
from collections import OrderedDict
import os
from django.conf import settings
from django.template import loader
from contents.models import ContentCategory
from goods.models import GoodsChannel

# 定时任务
def get_categories():
    # 拼装满足界面显示需求的数据格式： 商品频道及分类菜单
    ordered_dict = OrderedDict()
    channels = GoodsChannel.objects.order_by('group_id', 'sequence')
    for channel in channels:  #
        group_id = channel.group_id  # 第n组
        if group_id not in ordered_dict:
            group_dict = {'channels': [], 'sub_cats': []}
            ordered_dict[group_id] = group_dict
        else:
            group_dict = ordered_dict[group_id]

        # 一级类别:  {'id':, 'name':, 'url':}
        cat1 = channel.category
        cat1.url = channel.url  # 类别对象新增url属性
        group_dict['channels'].append(cat1)

        # 二级类别: {'id':, 'name':, 'sub_cats': [{}, {}, {}...]}
        for cat2 in cat1.goodscategory_set.all():
            cat2.sub_cats = []  # 对象新增sub_cats属性
            # 三级类别
            for cat3 in cat2.goodscategory_set.all():
                cat2.sub_cats.append(cat3)
            group_dict['sub_cats'].append(cat2)  # 添加二级类别

    return ordered_dict


# 定时任务
def generate_static_index_html():
    """生成静态的index.html"""
    print('%s: generate_static_index_html' % time.ctime())  # import time

    # 1. 获取类别数据
    ordered_dict = get_categories()
    # print(ordered_dict)

    # 2. 获取广告内容
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        # 一查多语法: cat.content_set.all()
        contents[cat.key] = cat.content_set.all().filter(
            status=True).order_by('sequence')

    # 3. 使用django模型语法渲染模板,得到静态的首页内容
    context = {
        'categories': ordered_dict, # {''}
        'contents': contents
    }
    template = loader.get_template('index.html')
    html_text = template.render(context)

    # 4. 把首页内容写到 front_end_pc/index.html 文件中
    file_path = os.path.join(settings.GENERATED_STATIC_HTML_FILES_DIR, 'index.html')
    with open(file_path, 'w') as f:
        f.write(html_text)