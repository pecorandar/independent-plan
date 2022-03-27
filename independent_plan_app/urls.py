from django.urls import path
from . import views
from django_distill import distill_path
from django.conf import settings
import requests
import math

from pprint import pprint 

app_name = 'independent_plan_app'

limit = 10  # 一覧ページに表示する記事数
url = getattr(settings, "BASE_URL", None)
api_key = getattr(settings, "API_KEY", None)
headers = {'X-MICROCMS-API-KEY': api_key}


def _post_total_count():
    """ポストAPIのトータル数を返す"""
    return requests.request(method='GET',
                            url=url + '/post',
                            headers=headers).json()['totalCount']


def _tag_total_count():
    """タグAPIのトータル数を返す"""
    return requests.request(method='GET',
                            url=url + '/tag',
                            headers=headers).json()['totalCount']


def get_category():
    res = requests.request(method='GET',
                            url=url + '/category',
                            headers=headers)
    
    for data in res.json()['contents']:
        if data['parentcategory'] is not None:
            continue
        yield data['category']


def get_subcategory():
    print('get_category ' * 10)
    res = requests.request(method='GET',
                            url=url + '/category',
                            headers=headers)
    for cat in get_category():
        for data in res.json()['contents']:
            if data['parentcategory'] is None:
                continue
            if data['parentcategory']["category"] == cat:
                yield {'category': cat, 'subcategory': data['category']}


def get_index():
    """
    トップページ
    引数はないので、Noneを返す
    """
    return None


def get_posts():
    """
    記事詳細ページを生成するためのpost idを返す

    """
    post_total_count = _post_total_count() 
    end_point = f'/post?limit={post_total_count}&fields=id'
    res = requests.request('GET', url=url + end_point, headers=headers) 

    for data in res.json()['contents']:
        yield data['id']


def get_pages():
    """
    ページ数を指定した一覧ページを生成するためのページ数を返す
    """
    post_total_count = _post_total_count()
    num_page = math.ceil(post_total_count / limit)
    for page_num in range(1, num_page + 1):
        yield {'page': str(page_num)}


def get_tags():
    """
    タグとページ数を指定した一覧ページを生成するための
    タグ＋ページ数を返す
    """
    tag_total_count = _tag_total_count()
    post_total_count = _post_total_count()
    # タグの一覧を取得
    end_point = f'/tag?limit={tag_total_count}&fields=id'
    tag_res = requests.request(method='GET',
                               url=url + end_point,
                               headers=headers)

    for data in tag_res.json()['contents']:
        # タグIDを取得
        tag_id = data['id']
        # タグに紐づく記事が何個あるか？を取得
        res = requests.request(method='GET',
                               url=url + f'/post?limit={post_total_count}&filters=tag[contains]{tag_id}',
                               headers=headers)
        post_total_count_with_tag = res.json()['totalCount']
        # 一ページあたりの記事数で割り出して、何ページあるか？を計算
        num_page = math.ceil(post_total_count_with_tag / limit)
        # タグIDとページ数をyield
        for page_num in range(1, num_page + 1):
            yield {'tag_id': tag_id, 'page': str(page_num)}


urlpatterns = [
    # トップページ カテゴリのindex.
    distill_path('', 
                 views.post_category,
                 name='index',
                 distill_file='index.html'),

    # カテゴリ サブカテゴリindex. そのカテゴリの記事．
    distill_path('category/<str:category>',
                 views.post_subcategory,
                 name='category',
                 distill_func=get_category),

    # 　サブカテゴリindex.
    distill_path('category/<str:category>/<str:subcategory>',
                 views.post_subcategory,
                 name='subcategory',
                 distill_func=get_subcategory),

    # 記事詳細ページ
    distill_path('post/<slug:slug>/',
                 views.post_detail,
                 name='post_detail',
                 distill_func=get_posts),

    # ページを指定した記事一覧
    distill_path('page/<str:page>/',
                 views.post_subcategory,
                 name='index_with_page',
                 distill_func=get_pages),

    # タグを指定した記事一覧
    distill_path('tag/<str:tag_id>/page/<str:page>/',
                 views.post_subcategory,
                 name='index_with_tag',
                 distill_func=get_tags),
]
