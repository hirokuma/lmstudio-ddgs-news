# DuckDuckGoでニュースを検索してLM Studioでまとめる

[mistralai/ministral-3-3b](https://lmstudio.ai/models/mistralai/ministral-3-3b)を動かしていた。

```shell
$ pip install -r requirements.txt 
...略...
$ cp env .env
$ python main.py 
最新ニュース(セキュリティ, 期間:1週間)を検索中...
ローカルLLMで解析中...

--- 解析結果 ---
以下は、2026年5月3日以降、1週間以内に発生した「セキュリティ」に関する事項です。

*   5月3日9時23分頃、石川県に高潮注意報が発表された（記事1）
*   4月30日に、Mythosをめぐる地政学をさらに複雑化させるニュースが飛び込んできた（記事2）
*   5月3日8時22分頃、天塩警察署が天塩郡天塩町字タツネウシで発生した事件・防犯等に関する情報を公開した（記事3）
```
