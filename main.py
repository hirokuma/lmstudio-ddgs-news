from openai import OpenAI
from ddgs import DDGS
from datetime import datetime
from pathlib import Path
import os
from dotenv import load_dotenv

# .envファイルが存在するかチェック
if not os.path.exists('.env'):
    print("警告: .envファイルが見つかりません。プログラムを終了します。")
    exit()

# .envファイルを読み込む
load_dotenv()

# 1. LM Studio サーバーの設定
OUT_FILENAME = os.getenv("OUT_FILENAME")
BASE_URL = os.getenv("BASE_URL")
API_KEY = os.getenv("API_KEY")
SEARCH = os.getenv("SEARCH")
QUERY = os.getenv("QUERY")
SPAN = os.getenv("SPAN")
NUM = int(os.getenv("NUM"))

# Base URLをLM Studioのローカルホストに指定
client = OpenAI(base_url=BASE_URL, api_key=API_KEY)

TIMELIMIT="w"
TIMEWORD="1週間"
if SPAN == "week":
    # 一週間
    TIMELIMIT="w"
    TIMEWORD="1週間"
elif SPAN == "month":
    # 一ヶ月
    TIMELIMIT="m"
    TIMEWORD="一ヶ月"
else:
    print(f"警告: SPAN設定が正しくありません({SPAN})")
    exit()

def get_news():
    news_context = ""
    # https://github.com/deedy5/ddgs#4-news
    with DDGS() as ddgs:
        results = ddgs.news(
            query=f"{SEARCH} {QUERY}",
            region="jp-jp",
            safesearch="off",
            timelimit=TIMELIMIT
        )
        
        for i, r in enumerate(results):
            if i >= NUM: break
            news_context += f"【記事{i+1}】\nタイトル: {r['title']}\n内容: {r['body']}\n\n"
    
    return news_context

def main():
    # 最新ニュースの取得
    print(f"最新ニュース({SEARCH}, 期間:{TIMEWORD})を検索中...")
    context = get_news()
    
    if not context:
        print("新しいニュースは見つかりませんでした。")
        return

    # 2. ローカルLLMへのプロンプト作成
    system_instruction = "提供されたニュースを分析し、事実のみを簡潔にまとめてください。"
    
    user_prompt = f"""
今日は {datetime.now().strftime('%Y-%m-%d')} です。
以下の最新ニュースから、過去{TIMEWORD}以内に発生した「{SEARCH}」のみを抽出してください。
{TIMEWORD}より前の古いニュースや一般的な情報は除外してください。

【ニュースデータ】
{context}
"""

    print("ローカルLLMで解析中...")
    try:
        response = client.chat.completions.create(
            model="model-identifier",
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3, # ニュース要約なので低めに設定
        )
        content = response.choices[0].message.content

        # 3. 結果の表示
        print("\n--- 解析結果 ---")
        print(content)

        # テキストファイルに保存
        txt_output_path = Path(__file__).parent / OUT_FILENAME
        with open(txt_output_path, 'w', encoding='utf-8') as f:
            f.write(content)

    except Exception as e:
        print(f"エラーが発生しました: {e}")

if __name__ == "__main__":
    main()