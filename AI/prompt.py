
def code_English_to_chinese(message):
    a="""
<rule>
<code>内的是代码片段，你需要将代码片段中的 // 和 /**/ 内的内容翻译成中文
***注意***
1，不能增添任何代码，不要多输出特殊符号，不要多输出空格，不能少输出任何源代码
2，不要输出<code>xml标签，不需要用```包裹
3、不要翻译代码！！！
</rule>
<code>
"""+message+"\n</code>"
    return a








