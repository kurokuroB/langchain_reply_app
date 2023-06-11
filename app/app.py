from flask import Flask, render_template, request
from langchain import OpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

app = Flask(__name__)

#グローバル変数
MODEL = "text-davinci-003"

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
    response=conversation("【】で囲まれた文章に対して、文体Aで返信文を作成してください。" + "【" + sentence + "】")

    # 履歴削除
    conversation.memory.clear()
    
    return render_template("result.html", title="結果画面", result=response['response'])


if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0') #host='0.0.0.0'で外部公開を行う
