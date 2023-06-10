from flask import Flask, render_template, request
from langchain import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

app = Flask(__name__)

#グローバル変数
MODEL = "text-davinci-003"
INSTRUCTION="""
【】で囲まれた文章に、以下の操作を加えてください。

操作１：誤字脱字を修正してください。
操作２：不適切な表現があれば、修正してください。
操作３：文体Aのような表現で書き直してください。
                      
操作後の文章のみを改行込みで出力してください。
出力する文章は【】で囲わないようにしてください。
また、それ以外の記号や文章は出力しないようにしてください。
                      
操作後の文章のみを改行込みで出力してください。
出力する文章は【】で囲わないようにしてください。
"""

# 会話用のインスタンスconversationを作成

llm = OpenAI(model_name=MODEL, max_tokens=1024) #出力文字数を多めに取る。デフォルトは256で少ない。
conversation = ConversationChain(llm=llm, verbose=False, memory=ConversationBufferMemory())


@app.route("/")
def index():
    return render_template("form.html", title="入力画面")


@app.route("/result", methods=["POST"])
def proofreading():
    style = request.form["style"]
    sentence = request.form["sentence"]
    
    # styleの記憶
    _ = conversation("【】で囲まれた文章の文体は文体Aです。" + "【" + style + "】")
    
    # 校正
    response=conversation(INSTRUCTION + "【" + sentence + "】")

    # 履歴削除
    conversation.memory.clear()
    
    return render_template("result.html", title="校正結果", result=response['response'])


if __name__ == "__main__":
    app.run(port=5000)
