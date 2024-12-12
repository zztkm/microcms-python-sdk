# microCMS Python SDK

[microCMS](https://microcms.io/) sdk for Python.

注意

- この SDK は非公式です
- この SDK は開発中なので、今後 API に破壊的変更が入る可能性があります

## Install

現在は PyPI に登録していないため、以下のコマンドでインストールしてください。

```bash
# pip を利用している場合
pip install git+https://github.com/zztkm/microcms-python-sdk.git

# uv を利用している場合
uv add https://github.com/zztkm/microcms-python-sdk.git
```

## APIs

コンテンツAPI

- [x] [GET /api/v1/{endpoint}](https://document.microcms.io/content-api/get-list-contents)
- [x] [GET /api/v1/{endpoint}/{content_id}](https://document.microcms.io/content-api/get-content)
- [ ] [POST /api/v1/{endpoint}](https://document.microcms.io/content-api/post-content)
- [ ] [PUT /api/v1/{endpoint}/{content_id}](https://document.microcms.io/content-api/put-content)
- [ ] [PATCH /api/v1/{endpoint}/{content_id}](https://document.microcms.io/content-api/patch-content)
- [ ] [DELETE /api/v1/{endpoint}/{content_id}](https://document.microcms.io/content-api/delete-content)

マネジメントAPI

- [ ] [GET /api/v1/contents/{endpoint}](https://document.microcms.io/management-api/get-list-contents-management)
- [ ] [GET /api/v1/contents/{endpoint}/{content_id}](https://document.microcms.io/management-api/get-content)
- [ ] [PATCH /api/v1/contents/{endpoint}/{content_id}/status](https://document.microcms.io/management-api/patch-contents-status)
- [ ] [GET /api/v1/media](https://document.microcms.io/management-api/get-media)
