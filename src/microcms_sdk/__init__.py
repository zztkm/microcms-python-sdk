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

    def get(self, endpoint: str) -> Any:
        """Get data from the specified endpoint.

        :param endpoint: The endpoint to get data from.
        :return: The data returned by the endpoint.
        """
        # 当初はユーザー定義のオブジェクトにジェネリクスを活用しようと考えていたが
        # contents 内のデータをパースしたい場合に SDK レイヤーでは難しいため
        # ユーザー定義のオブジェクトは Any で統一しておき、ユーザー側で処理してもらう方針にした
        r = self.client.get(f"/v1/{endpoint}")
        if r.status_code != httpx.codes.OK:
            raise Exception(f"Failed to get {endpoint}: {r.status_code} {r.text}")

        # 返却値がリスト形式か、単一のオブジェクト形式かを判定して
        # リスト形式であれば totalCount, offset, limit をサービスが付与するので
        # その部分は事前定義の dataclass に格納して返却するようにしてみようと思ったが
        # 判定の仕方がレスポンスボディに totalCount, offset, limit が存在するかどうかでしかないため
        # 仮にユーザーがそのようなフィールドを持つオブジェクトを作成してしまった場合に、間違った処理
        # を行ってしまう可能性があるため、返却値をそのまま返却することにした
        # response header に api_type みたいなの入ってくればよいのに...
        return r.json()
