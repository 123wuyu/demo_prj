from flask_restful import Resource, inputs
from flask_restful.reqparse import RequestParser
from flask import current_app

from . import constants
from models.news import Article
from cache import article as cache_article


class SearchResource(Resource):
    """
    搜索
    """
    # GET /search?q=用户输入的关键词&page=xxx&per_page=xxx

    def get(self):
        # 检验参数
        rp = RequestParser()
        rp.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
        rp.add_argument('page', type=inputs.positive, required=False, location='args')
        rp.add_argument('per_page', type=inputs.int_range(constants.SEARCH_RESULTS_PER_PAGE_MIN,
                                                          constants.SEARCH_RESULTS_PER_PAGE_MAX),
                        required=False, location='args')

        req = rp.parse_args()
        q = req.q
        page = 1 if not req.page else req.page
        per_page = constants.SEARCH_RESULTS_PER_PAGE_MIN if not req.per_page else req.per_page

        # 业务处理
        #  1. 查询es 获取搜索结果  文章id
        query_body = {
            "from": (page-1)*per_page,
            "size": per_page,
            "_source": ['article_id'],
            "query": {
                "bool": {
                    "must": {
                        "match": {
                            "_all": q
                        }
                    },
                    "filter": {
                        "term": {
                            "status": Article.STATUS.APPROVED
                        }
                    }
                }
            }

        }

        ret = current_app.es.search(index='articles', doc_type='article', body=query_body)

        # {
        #   "took" : 17,
        #   "timed_out" : false,
        #   "_shards" : {
        #     "total" : 3,
        #     "successful" : 3,
        #     "skipped" : 0,
        #     "failed" : 0
        #   },
        #   "hits" : {
        #     "total" : 107,
        #     "max_score" : 12.852392,
        #     "hits" : [
        #       {
        #         "_index" : "articles_v2",
        #         "_type" : "article",
        #         "_id" : "411",
        #         "_score" : 12.852392,
        #         "_source" : {
        #           "article_id" : 411
        #         }
        #       },

        # ret 就是es返回的json字符串转换成的python字典
        total_count = ret['hits']['total']  # 总条目数

        #  2. 根据文章id查询文章数据（缓存工具）
        results = []
        for item in ret['hits']['hits']:
            # article_id = item['_source']['article_id']
            article_id = item['_id']
            article_data = cache_article.ArticleInfoCache(article_id).get()
            results.append(article_data)
        # 返回
        return {'total_count': total_count, 'page': page, 'per_page': per_page, 'results': results}


class SuggestionResource(Resource):
    """
    联想建议
    """
    def get(self):
        """
        获取联想建议
        """
        qs_parser = RequestParser()
        qs_parser.add_argument('q', type=inputs.regex(r'^.{1,50}$'), required=True, location='args')
        args = qs_parser.parse_args()
        q = args.q

        # 先尝试自动补全建议查询
        query = {
            'from': 0,
            'size': 10,
            '_source': False,
            'suggest': {
                'word-completion': {
                    'prefix': q,
                    'completion': {
                        'field': 'suggest'
                    }
                }
            }
        }
        ret = current_app.es.search(index='completions', doc_type='words', body=query)
        options = ret['suggest']['word-completion'][0]['options']

        # 如果没得到查询结果，进行纠错建议查询
        if not options:
            query = {
                'from': 0,
                'size': 10,
                '_source': False,
                'suggest': {
                    'text': q,
                    'word-phrase': {
                        'phrase': {
                            'field': '_all',
                            'size': 1
                        }
                    }
                }
            }
            ret = current_app.es.search(index='articles', doc_type='article', body=query)
            options = ret['suggest']['word-phrase'][0]['options']

        results = []
        for option in options:
            if option['text'] not in results:
                results.append(option['text'])

        return {'options': results}