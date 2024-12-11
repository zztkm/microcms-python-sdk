import os
from dotenv import load_dotenv
from microcms_sdk import MicroCMSClient
from dataclasses import dataclass
from serde import serde, from_dict


load_dotenv()
# 使用例
microcms_api_key = os.environ["MICROCMS_API_KEY"]
microcms_api_url = os.environ["MICROCMS_API_URL"]


@dataclass
class MainConfig:
    createdAt: str
    updatedAt: str
    publishedAt: str
    revisedAt: str
    name: str


@serde
class ListConfigContent:
    id: str
    createdAt: str
    updatedAt: str
    publishedAt: str
    revisedAt: str
    name: str


@serde
class ListContentsResponse:
    contents: list[ListConfigContent]
    totalCount: int
    offset: int
    limit: int


client = MicroCMSClient(microcms_api_url, microcms_api_key)

# MainConfig にパースする
data = client.get("test")
main_config = MainConfig(**data)
print(main_config)

# ListContentsResponse にパースする
# リスト形式の場合、ネストしたデータクラスに対して自前でパースする処理を書くのは大変なので
# pyserde を利用することをおすすめします (もちろんオブジェクト形式の場合でも pyserde を利用しても良いです)
data = client.get("list_test")
list_config = from_dict(ListContentsResponse, data)
print(list_config.totalCount)
print(list_config.contents)
