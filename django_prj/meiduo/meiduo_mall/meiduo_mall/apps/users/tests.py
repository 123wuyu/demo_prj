from django.template import loader
from django.test import TestCase, Client
from wheel.signatures import assertTrue


def generate_test_html():
    """测试生成静态页面"""

    context = {
        'city': '北京',
        'adict': {
            'name': '西游记',
            'author': '吴承恩'
        },
        'alist': [1, 2, 3, 4, 5]
    }

    template = loader.get_template('test3.html')
    html_str = template.render(context)  # str
    print(html_str)

    # 保存生成 的静态内容到: front_end_pc/test3.html
    file_path = '/home/python/code/gz07/meiduo/front_end_pc/test3.html'
    with open(file_path, 'w') as file:
        file.write(html_str)

'''
class AnimalTestCase(TestCase):

    def setUp(self): # test_meiduo_mall
        Animal.objects.create(name="lion", sound="roar")
        Animal.objects.create(name="cat", sound="meow")

    def test_animals_can_speak(self):
        """Animals that can speak are correctly identified"""
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')
'''












