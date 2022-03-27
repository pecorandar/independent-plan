datas = {
    "contents": [{
            "id": "python",
            "createdAt": "2022-03-22T11:17:06.914Z",
            "updatedAt": "2022-03-23T17:26:37.518Z",
            "publishedAt": "2022-03-22T11:17:06.914Z",
            "revisedAt": "2022-03-22T11:17:06.914Z",
            "category": "python",
            "parentcategory": None
        },
        {
            "id": "matplotlib",
            "createdAt": "2022-03-23T17:26:00.453Z",
            "updatedAt": "2022-03-23T17:26:00.453Z",
            "publishedAt": "2022-03-23T17:26:00.453Z",
            "revisedAt": "2022-03-23T17:26:00.453Z",
            "category": "matplotlib",
            "parentcategory": {
                "id": "python",
                "createdAt": "2022-03-22T11:17:06.914Z",
                "updatedAt": "2022-03-23T17:26:37.518Z",
                "publishedAt": "2022-03-22T11:17:06.914Z",
                "revisedAt": "2022-03-22T11:17:06.914Z",
                "category": "python",
                "parentcategory": None
            }
        },
        {
            "id": "git",
            "createdAt": "2022-03-23T16:56:45.516Z",
            "updatedAt": "2022-03-26T10:57:56.058Z",
            "publishedAt": "2022-03-26T10:57:56.058Z",
            "revisedAt": "2022-03-26T10:57:56.058Z",
            "category": "git",
            "parentcategory": None
        },
        {
            "id": "javascript",
            "createdAt": "2022-03-22T11:19:13.663Z",
            "updatedAt": "2022-03-26T10:58:00.266Z",
            "publishedAt": "2022-03-26T10:58:00.266Z",
            "revisedAt": "2022-03-26T10:58:00.266Z",
            "category": "javascript",
            "parentcategory": None
        },
        {
            "id": "javascript-string",
            "createdAt": "2022-03-24T16:00:16.845Z",
            "updatedAt": "2022-03-26T10:59:36.048Z",
            "publishedAt": "2022-03-26T10:59:36.048Z",
            "revisedAt": "2022-03-26T10:59:36.048Z",
            "category": "string",
            "parentcategory": {
                "id": "javascript",
                "createdAt": "2022-03-22T11:19:13.663Z",
                "updatedAt": "2022-03-26T10:58:00.266Z",
                "publishedAt": "2022-03-26T10:58:00.266Z",
                "revisedAt": "2022-03-26T10:58:00.266Z",
                "category": "javascript",
                "parentcategory": None
            }
        },
        {
            "id": "javascript-regexp",
            "createdAt": "2022-03-24T16:48:39.527Z",
            "updatedAt": "2022-03-26T10:59:41.615Z",
            "publishedAt": "2022-03-26T10:59:41.615Z",
            "revisedAt": "2022-03-26T10:59:41.615Z",
            "category": "regexp",
            "parentcategory": {
                "id": "javascript",
                "createdAt": "2022-03-22T11:19:13.663Z",
                "updatedAt": "2022-03-26T10:58:00.266Z",
                "publishedAt": "2022-03-26T10:58:00.266Z",
                "revisedAt": "2022-03-26T10:58:00.266Z",
                "category": "javascript",
                "parentcategory": None
            }
        },
        {
            "id": "network",
            "createdAt": "2022-03-23T17:38:40.825Z",
            "updatedAt": "2022-03-26T11:32:47.489Z",
            "publishedAt": "2022-03-26T11:32:47.489Z",
            "revisedAt": "2022-03-26T11:32:47.489Z",
            "category": "network",
            "parentcategory": None
        }
    ],
    "totalCount": 7,
    "offset": 0,
    "limit": 10
}


def get_category():

    # pprint(res.json())

    for data in datas["contents"]:
        if data['parentcategory'] is not None:
            continue
        yield data['category']

for cat in get_category():
    for data in datas['contents']:
        if data['parentcategory'] is None:
            continue
        if data['parentcategory']["category"] == cat:
            print( {'category': cat, 'subcategory': data['category']})
            # yield {'category': cat, 'subcategory': data['category']}
