"""A Python SDK for the MicroCMS API."""

from typing import Any

import httpx


class MicroCMSClient:
    """A client for the MicroCMS API."""

    def __init__(self, base_url: str, api_key: str) -> None:
        """Initialize the MicroCMSClient with the given base URL and API key.

        :param base_url: The base URL for the MicroCMS API.
        :param api_key: The API key for authenticating requests.
        """
        self.client = httpx.Client(headers={"X-MICROCMS-API-KEY": api_key}, base_url=base_url)

    def get(
        self,
        endpoint: str,
        *,
        content_id: str | None = None,
        draft_key: str | None = None,
        fields: list[str] | None = None,
        depth: int | None = None,
        rich_editor_format: str | None = None,
    ) -> Any:
        """Get data from the specified endpoint.

        :param endpoint: API エンドポイント。
        :param content_id: リスト型APIにおいて、id 指定してコンテンツを取得したい場合に指定する。
        :param draft_key: 下書きのデータを取得する場合に指定する。
        :param fields: 取得するフィールドを指定する。
        :param depth: 取得するデータの深さを指定する。(microCMSのデフォルト値は1)
        :return: API から取得したデータを Python オブジェクトに変換したもの。

        NOTE: microCMS のデフォルト値を SDK に実装してしまうと万が一変更があった場合に対応
        しなければならなくなるので、デフォルト値は microCMS の仕様に任せる方針で実装している。

        TODO(zztkm): get と list_content は Query Params と content_id の有無以外は共通の処理になるので
        同じメソッドにまとめたほうが良いか検討する
        """
        params = self._parse_query_params(
            draft_key=draft_key,
            fields=fields,
            depth=depth,
            rich_editor_format=rich_editor_format,
        )
        if content_id:
            endpoint = f"{endpoint}/{content_id}"
        r = self.client.get(f"/v1/{endpoint}", params=params)
        if r.status_code != httpx.codes.OK:
            raise Exception(f"Failed to get {endpoint}: {r.status_code} {r.text}")

        # 当初はユーザー定義のオブジェクトにジェネリクスを活用しようと考えていたが
        # contents 内のデータをパースしたい場合に SDK レイヤーでは難しいため
        # ユーザー定義のオブジェクトは Any で統一しておき、ユーザー側で処理してもらう方針にした
        return r.json()

    def list_content(
        self,
        endpoint: str,
        *,
        draft_key: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        orders: list[str] | None = None,
        q: str | None = None,
        fields: list[str] | None = None,
        ids: list[str] | None = None,
        filters: str | None = None,
        depth: int | None = None,
        rich_editor_format: str | None = None,
    ) -> Any:
        params = self._parse_query_params(
            draft_key=draft_key,
            limit=limit,
            offset=offset,
            orders=orders,
            q=q,
            fields=fields,
            ids=ids,
            filters=filters,
            depth=depth,
            rich_editor_format=rich_editor_format,
        )
        r = self.client.get(f"/v1/{endpoint}", params=params)
        if r.status_code != httpx.codes.OK:
            raise Exception(f"Failed to list {endpoint}: {r.status_code} {r.text}")
        return r.json()

    def _parse_query_params(
        self,
        *,
        draft_key: str | None = None,
        limit: int | None = None,
        offset: int | None = None,
        orders: list[str] | None = None,
        q: str | None = None,
        fields: list[str] | None = None,
        ids: list[str] | None = None,
        filters: str | None = None,
        depth: int | None = None,
        rich_editor_format: str | None = None,
    ) -> dict[str, str | int] | None:
        # None でない引数のみを dict に格納して返却する
        # すべての引数が None の場合は None を返却する
        params: dict[str, str | int] = {}
        if draft_key:
            params["draftKey"] = draft_key
        if limit:
            params["limit"] = limit
        if offset:
            params["offset"] = offset
        if orders:
            params["orders"] = ",".join(orders)
        if q:
            params["q"] = q
        if ids:
            params["ids"] = ",".join(ids)
        if filters:
            params["filters"] = filters
        if fields:
            params["fields"] = ",".join(fields)
        if depth:
            params["depth"] = depth
        if rich_editor_format:
            params["richEditorFormat"] = rich_editor_format

        # dict が空の場合は None を返却する
        if len(params.keys()) == 0:
            return None

        return params
