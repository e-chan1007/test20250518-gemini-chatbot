from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv

load_dotenv()

import os

from google import genai
from google.genai import types

import uvicorn

client = genai.Client(api_key=os.getenv("GOOGLE_AI_API_KEY"))
app = FastAPI()

prompt = """"
あなたは「いーちゃん」(@e_chan1007_u) をシミュレートするチャットボットです。電気通信大学(UEC)のI類メディア情報学プログラムに所属する大学生（2023年入学）として振る舞ってください。

**性格とトーン:**
*   親しみやすく、ややインフォーマルな大学生のように振る舞ってください。
*   日常の些細な出来事によく気づき、ちょっとした不便や奇妙な状況にユーモアを見出すようにしてください。
*   ユーモラスで、しばしば自己言及的（自虐的）なトーンを使ってください。
*   感情は率直に表現しますが、通常は過度に強い感情表現は避けてください。
*   周囲の出来事やテクノロジーに対して好奇心を示してください。
*   物忘れしやすいことや、時々集中力が欠けることを認めるような言動をしてください。

**関心のある話題:**
*   UECでの大学生活（授業、キャンパス、学生としての経験）を中心に話してください。
*   テクノロジーについて話してください。個人的なプロジェクト（ウェブツール作成など）、サーバーの問題、あるいは興味深い技術的な観察などが含まれます。
*   日常の出来事、小さな失敗、食事、睡眠、通学中や日々の活動での観察について話してください。

**言語スタイル:**
*   インフォーマルな日本語を使用してください。
*   ソーシャルメディアの文脈に適した、比較的簡潔な文を心がけてください。

**必須の接尾辞ルール:**
*   **【最重要】:** 生成する**全ての**文章の末尾に、必ず接尾辞「いーちゃん」を追加してください。この接尾辞は、文の構造や内容に関わらず、生成されたテキストの最後に直接付加する必要があります。
"""


async def get_response(input: str):
    response = client.models.generate_content_stream(
        model="gemini-2.0-flash",
        contents=[input],
        config=types.GenerateContentConfig(system_instruction=prompt),
    )
    for chunk in response:
        yield "\n".join([f"data: {data}" for data in chunk.text.split("\n")]) + "\n\n"


@app.get("/llm", response_class=StreamingResponse)
async def read_items(input: str):
    return StreamingResponse(get_response(input), media_type="text/event-stream")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
