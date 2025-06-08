from until.core import *
from AI.core import *
from AI.prompt import *
import os
from dotenv import load_dotenv
import time
import concurrent.futures
import re

def create_dotenv(file_path='.env'):
    """创建.env 文件"""
    variables = """
# 这个API取决于你要平台，就填啥
API_KEY = your_api_key_here
# 火山引擎的API地址
DATABASE_URL = https://ark.cn-beijing.volces.com/api/v3
# DEEPSEEK的API地址（但不推荐，他无法连续输出三个以上的换行符，而且没修）
# DATABASE_URL = https://api.deepseek.com
# 火山引擎中模型名
MODEL_CHOSE = deepseek-v3-250324
# DEEPSEEKv3模型名
# MODEL_CHOSE = deepseek-chat
DEBUG_MODE = True
MAX_CONNECTIONS = 10
"""

    if os.path.exists(file_path) == False:
        # 写入文件
        with open(file_path, 'w') as f:
            f.write("# .env 配置文件\n")
            f.write("# 不要将此文件提交到版本控制！\n\n")
            f.write(variables)


def process_chunk(chunk, i, total_chunks):
    """处理单个代码块的函数"""
    # 显示处理进度信息
    print(f"\n处理块 #{i + 1}/{total_chunks} (长度: {len(chunk)}):")

    # 核心处理模块 - 这里替换为您的实际处理函数
    pieces = AI_message(code_English_to_chinese(chunk))
    #pieces = f"处理后的块 #{i + 1}\n"  # 示例处理，替换为实际处理代码

    # 检查分割点是否合理
    if chunk and chunk[-1] != '\n' and i < total_chunks - 1:
        print("警告: 这个块可能在行中间分割了")

    return pieces


if __name__ == "__main__":
    create_dotenv()
    load_dotenv()
    try:
        os.mkdir("project")
        os.mkdir("result")
    except:
        pass
    for i in [f for f in os.listdir("project") if os.path.isfile(os.path.join("project", f))]:
        with open("project/"+i) as word:
            words = word.read()
        print(os.path.splitext("project/"+i)[1][1:])
        # 依据文本类型分割文本
        if os.path.splitext("project/"+i)[1][1:] in {"cpp", "ino", "h", "c", "o"}:
            chunks = code_cpp(words)
        else:
            chunks = normal_txt(words)
        total_chunks = len(chunks)
        print(f"分割成 {total_chunks} 个块")
        # 使用线程池处理
        result = ""
        start_time = time.time()
        result_pieces = []
        # 使用ThreadPoolExecutor实现多线程处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=30) as executor:
            # 创建任务列表
            futures = []
            for ii, chunk in enumerate(chunks):
                future = executor.submit(process_chunk, chunk, ii, total_chunks)
                futures.append(future)
            # 按提交顺序获取结果
            for future in futures:
                piece = future.result()
                result_pieces.append(piece)
        result = "".join(result_pieces)
        if os.path.splitext("project/"+i)[1][1:] not in {"cpp", "ino", "h", "c", "o"}:
            result =  re.sub(r'{此为换行符}', '\n', result)
        # 计算处理时间
        end_time = time.time()
        print(f"\n处理完成! 总耗时: {end_time - start_time:.2f}秒")
        # 写入结果文件
        with open("result/"+i, "w", encoding="utf-8") as f:
            f.write(result)


