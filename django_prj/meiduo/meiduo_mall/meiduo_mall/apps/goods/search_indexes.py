from haystack import indexes

from goods.models import SKU


class SKUIndex(indexes.SearchIndex, indexes.Indexable):
    """商品索引类"""

    # 组合字段(id name caption: 商品副标题)
    # text: 名字固定
    text = indexes.CharField(document=True, use_template=True)

    # 单一字段
    id = indexes.IntegerField(model_attr='id')
    name = indexes.CharField(model_attr='name')
    price = indexes.DecimalField(model_attr='price')
    default_image_url = indexes.CharField(model_attr='default_image_url')
    comments = indexes.IntegerField(model_attr='comments')

    def get_model(self):
        # 针对商品表生成索引库
        return SKU

    def index_queryset(self, using=None):
        """需要根据数据库表的哪些数据来创建索引"""
        # return self.get_model().objects.filter(is_launched=True)
        return SKU.objects.filter(is_launched=True)  # 针对上架的商品创建索引























