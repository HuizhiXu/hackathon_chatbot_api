import gradio as gr
import os
import openai
import langchain

# 请记得要把 api 的 key 放到 settings 下面的 Repository Secrets 里。

from langchain import OpenAI, LLMChain, PromptTemplate

openai.api_key = os.getenv("openai_key")

# 如果你只打算通过 prompt 来定制机器人的行为，只需要修改这段 prompt 就够了。
# 不能包含输入的字不能包含输入的字不能包含输入的字重要的事情说三次哪怕是单字也不行。
prompt = """我们现在正在玩《你比划我猜》的游戏，请你对输入进行描述，让别人能够猜出来你说的是什么。有几点要求：
        1. 首先你要说出输入的长度是什么，格式为：词语为n个字。
        2. 你的描述不能包含输入的字。如果你的描述包含输入词语，那我会给你打零分哦。例如输入是"我们的故事"，那么你的描述不能有"我"，"们"，"的"，"故"，"事"这几个字。
        3. 要求你的语言风格是萌妹或硬汉的风格，尽量口语化，也可以使用颜文字和语气词。
        
           """

history = {}

# prompt = PromptTemplate(
#     template=template,
#     input_variables=['text']
# )

# llm_chain = LLMChain(
#     prompt=prompt,
#     llm="gpt-3.5-turbo"
# )
# print(llm_chain)
#
# llm_chain = LLMChain(
#     llm=OpenAI(),
#     prompt=prompt,
# # llm="gpt-3.5-turbo"
#     # verbose=True,
# )

# print(llm_chain.run(question))

# 修改本函数，来实现你自己的 chatbot
# p: 对机器人说话的内容  
# qid: 当前消息的唯一标识。例如 `'bxqid-cManAtRMszw...'`。由平台生成并传递给机器人，以便机器人区分单个问题（写日志、追踪调试、异步回调等）。同步调用可忽略。  
# uid: 用户的唯一标识。例如`'bxuid-Aj8Spso8Xsp...'`。由平台生成并传递给机器人，以便机器人区分用户。可被用于实现多轮对话的功能。  
# 返回值：[type, content]
# 详见 https://huggingface.co/spaces/baixing/hackathon_test/blob/main/bot-api.md
def chat(p, qid, uid):
    # 找出该 uid 对应的历史对话
    global history
    if uid in history:
        msgs = history[uid]
    else:
        msgs = []

    response = callapi(p, msgs)
    history[uid] = msgs + [[p, response]]
    return ["text", response]


def callapi(p, msgs):
    if (len(msgs) > 8):  # 简单 hard-code 8 回合对话。如果需要更精准的，应该计算 token 数
        msgs = msgs[-8:]

    data = [{"role": "system", "content": prompt}]
    for m in msgs:
        data = data + [
            {"role": "user", "content": m[0]},
            {"role": "assistant", "content": m[1]}
        ]
    data = data + [{"role": "user", "content": p}]


    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=data
    )
    print(response)
    response = response["choices"][0]["message"]["content"]
    while response.startswith("\n"):
        response = response[1:]
    return response


iface = gr.Interface(fn=chat,
                     inputs=["text", "text", "text"],
                     outputs=["text", "text"],
                     description="""这个机器人可以帮你在玩《你比划我猜》大显身手，用萌妹或者硬汉的风格对词语进行描述。
[对话测试](https://huggingface.co/spaces/BaixingAI/hackathon_test)   [参考文档](https://huggingface.co/spaces/baixing/hackathon_test/blob/main/bot-api.md)    [Q & A](https://huggingface.co/spaces/baixing/hackathon_test/blob/main/qna.md)
                     """)
iface.launch()
