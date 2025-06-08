from openai import OpenAI
import base64
import io
import os

def AI_image(question,image):
    # 转发给AI前的预处理
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG")  # 或使用 "PNG" 等格式
    img_bytes = buffer.getvalue()
    base64_str = base64.b64encode(img_bytes).decode("utf-8")
    data_uri = f"data:image/jpeg;base64,{base64_str}"
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url=os.getenv("DATABASE_URL"),
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=os.getenv("API_KEY"),
    )
    response = client.chat.completions.create(
        model="doubao-1.5-vision-pro-250328",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri}
                    },
                    {"type": "text", "text": question}  # 替换为你的文本问题
                ]
            }
        ]
    )
    return response

def AI_message(question):
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url=os.getenv("DATABASE_URL"),
        # 从环境变量中获取您的 API Key。此为默认方式，您可根据需要进行修改
        api_key=os.getenv("API_KEY")
    )
    response = client.chat.completions.create(
        model=os.getenv("MODEL_CHOSE"),
        messages=[
          {"role": "system", "content":"现在你是一个AI工具"},
          {"role": "user", "content":question}
        ],
    stream = False
    )
    return "\n"+response.choices[0].message.content

def AI_chose():
    client = OpenAI(
        # 此为默认路径，您可根据业务所在地域进行配置
        base_url="https://ark.cn-beijing.volces.com/api/v3",
        # 从环境变量中获取您的 API Key
        api_key=api_key,
    )

    # Non-streaming:
    print("----- standard request -----")
    completion = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="deepseek-v3-250324",
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": "你好"},
        ],
    )
    print(completion.choices[0].message.content)

    # Streaming:
    print("----- streaming request -----")
    stream = client.chat.completions.create(
        # 指定您创建的方舟推理接入点 ID，此处已帮您修改为您的推理接入点 ID
        model="deepseek-v3-250324",
        messages=[
            {"role": "system", "content": "你是人工智能助手"},
            {"role": "user", "content": "你好"},
        ],
        # 响应内容是否流式返回
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        print(chunk.choices[0].delta.content, end="")
    print()

