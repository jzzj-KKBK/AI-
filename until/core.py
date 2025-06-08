import re

def code_cpp(text, chunk_size=2000, delimiters='}"\',;:!?)>] \t\n'):
    """
    将代码文本分割成指定大小的块，分割点尽量靠近特殊字符，并确保整行完整性

    参数:
        text: 要分割的文本
        chunk_size: 目标块大小(默认2000字符)
        delimiters: 优先分割的特殊字符(默认包含各种编程符号)

    返回:
        分割后的文本块列表
    """
    text = re.sub(r'\n{3,}', '\n\n', text)
    chunks = []
    start = 0
    n = len(text)

    while start < n:
        # 计算当前块的结束位置
        end = min(start + chunk_size, n)

        # 如果已经到文本末尾
        if end == n:
            chunks.append(text[start:])
            break

        # 查找下一个换行符以确保整行完整
        newline_pos = text.find('\n', end)

        if newline_pos != -1 and newline_pos < end + 100:
            # 如果换行符在合理范围内，优先在换行符后分割
            split_pos = newline_pos + 1
            chunks.append(text[start:split_pos])
            start = split_pos
            continue

        # 向前查找最近的分隔符
        split_pos = end
        for i in range(end, min(end + 300, n)):  # 向后查找最多300字符
            if text[i] in delimiters:
                split_pos = i + 1  # 在分隔符后分割
                break

        # 如果向后没找到，尝试查找换行符
        if split_pos == end:
            newline_pos = text.find('\n', end)
            if newline_pos != -1 and newline_pos < end + 300:
                split_pos = newline_pos + 1

        # 如果向后没找到换行符，向前查找分隔符
        if split_pos == end:
            for i in range(end, max(start, end - 300) - 1, -1):  # 向前查找最多300字符
                if text[i] in delimiters:
                    split_pos = i + 1
                    break

        # 添加当前块并更新起始位置
        chunks.append(text[start:split_pos])
        start = split_pos

    return chunks
def normal_txt(text, chunk_size=2000, delimiters='.。，, \t\n'):
    text = re.sub(r'\n', '{此为换行符}', text)
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        # 计算当前块的结束位置
        end = min(start + chunk_size, n)

        # 如果已经到文本末尾
        if end == n:
            chunks.append(text[start:])
            break

        # 查找下一个换行符以确保整行完整
        newline_pos = text.find('\n', end)

        if newline_pos != -1 and newline_pos < end + 100:
            # 如果换行符在合理范围内，优先在换行符后分割
            split_pos = newline_pos + 1
            chunks.append(text[start:split_pos])
            start = split_pos
            continue

        # 向前查找最近的分隔符
        split_pos = end
        for i in range(end, min(end + 300, n)):  # 向后查找最多300字符
            if text[i] in delimiters:
                split_pos = i + 1  # 在分隔符后分割
                break

        # 如果向后没找到，尝试查找换行符
        if split_pos == end:
            newline_pos = text.find('\n', end)
            if newline_pos != -1 and newline_pos < end + 300:
                split_pos = newline_pos + 1

        # 如果向后没找到换行符，向前查找分隔符
        if split_pos == end:
            for i in range(end, max(start, end - 300) - 1, -1):  # 向前查找最多300字符
                if text[i] in delimiters:
                    split_pos = i + 1
                    break

        # 添加当前块并更新起始位置
        chunks.append(text[start:split_pos])
        start = split_pos

    return chunks

