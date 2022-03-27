from http.client import HTTPResponse
from turtle import pos
from django.shortcuts import render

from django.shortcuts import render
import requests
from django.conf import settings
from django.http import Http404
import math


from pprint import pprint



def post_category(request, **kwargs):
    """カテゴリ一覧"""
    print('kwargs', kwargs)
    print('kwargs', kwargs)
    print('kwargs', kwargs)


    end_point = f'/category'

    url = getattr(settings, "BASE_URL", None)
    api_key = getattr(settings, "API_KEY", None)
    headers = {'X-MICROCMS-API-KEY': api_key}
    res = requests.request(method='GET',
                           url=url + end_point,
                           headers=headers)
    # タグの一覧を取得
    tags_res = requests.request(method='GET',
                                url=url + '/tag',
                                headers=headers)
    # 名前昇順で並び替え
    tag_list = tags_res.json()['contents']
    tag_list.sort(key=lambda x: x['name'])

    cats = res.json()['contents']
    context = {
        'categories': [{'category': cat,
                        'sub_categories': [sub_cat for sub_cat in cats 
                                        if sub_cat.get('parentcategory') is not None \
                                        and sub_cat.get('parentcategory').get('category') == cat.get('category')]}
                            for cat in cats if cat.get('parentcategory') is None],
        # トップページの一覧用
        'tag_list': tag_list,
    }
    return render(request, 'independent_plan/index.html', context)


def post_subcategory(request, **kwargs):
    """記事一覧"""

    print('post_subcat', kwargs)
    print('post_subcat', kwargs)
    print('post_subcat', kwargs)
    print('post_subcat', kwargs)
    
    limit = 10
    current_page = kwargs.get('page', 1)
    offset = (int(current_page) - 1) * limit

    end_point = f'/post?limit={limit}&offset={offset}'

    # タグIDが渡された場合はエンドポイントを更新
    tag_id = kwargs.get('tag_id', None)
    if tag_id:
        end_point += f'&filters=tag[contains]{tag_id}'

    url = getattr(settings, "BASE_URL", None)
    api_key = getattr(settings, "API_KEY", None)
    headers = {'X-MICROCMS-API-KEY': api_key}

    # タグの一覧を取得
    tags_res = requests.request(method='GET',
                                url=url + '/tag',
                                headers=headers)
    # 名前昇順で並び替え
    tag_list = tags_res.json()['contents']
    tag_list.sort(key=lambda x: x['name'])

    # とりあえずcategoryなし以外のpostを持ってくる．
    end_point += '&filters=category[exists]'
    res = requests.request(method='GET',
                           url=url + end_point,
                           headers=headers)
    

    cat_id = kwargs.get('category')
    sub_cat_id = kwargs.get('sabcategory')


    posts_list = res.json()['contents']
    if sub_cat_id is not None:
        # sub_catがある場合，自身のカテゴリのidがsub_catと一致するpostのみ
        post_list = [post for post in posts_list
                        if post.get('category').get('id') == sub_cat_id]
    else:
        # subがない場合，自身のカテゴリか，自身のカテゴリの親カテゴリのidがcatに一致するpost
        post_list = [post for post in posts_list
                        if post.get('category').get('id') == cat_id or (
                            isinstance(post.get('category').get('parentcategory'), dict) \
                            and post.get('category').get('parentcategory').get('id') == cat_id)]
    
    total_count = res.json()['totalCount']
    num_page = math.ceil(total_count / limit)

    context = {
        'cat_title': cat_id,
        'post_list': post_list,
        'num_page': range(1, num_page + 1),
        'current_page': int(current_page),
        'last_page': num_page,
        # トップページの一覧用
        'tag_list': tag_list,
        # ページャーの処理用
        'tag_id': tag_id
    }
    return render(request, 'independent_plan/category_index.html', context)


def post_detail(request, slug):
    """記事詳細"""
    end_point = f'/post/{slug}'
    url = getattr(settings, "BASE_URL", None)
    api_key = getattr(settings, "API_KEY", None)
    headers = {'X-MICROCMS-API-KEY': api_key}
    res = requests.request('GET', url=url + end_point, headers=headers)
    # ステータスコード200以外はエラーなので、404表示
    if res.status_code != 200:
        raise Http404
    context = {
        'post': res.json()
    }

    return render(request, 'independent_plan/post_detail.html', context)

