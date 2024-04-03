import streamlit as st

# 假设成语列表存储在一个文件中，每行一个成语
idioms_file = "idioms.txt"


# 读取成语列表
def read_idioms():
    with open(idioms_file, "r", encoding="utf-8") as f:
        idioms = [line.strip() for line in f.readlines()]
    return idioms


# 匹配成语
def match_idioms(user_input, idioms):
    matched_idioms = []

    # 将用户输入的每个字逐个与成语列表中的成语进行匹配
    for idiom in idioms:
        idiom_chars = set(idiom)
        user_input_chars = set(user_input)
        # 如果成语中的每个字都在用户输入中出现，则认为匹配成功
        if user_input_chars.issuperset(idiom_chars):
            matched_idioms.append(idiom)

    return matched_idioms


# 设置页面标题
st.title("成语匹配器")

# 读取成语列表
idioms_list = read_idioms()

# 添加输入框和按钮
user_input = st.text_input("请输入成语")
search_button = st.button("搜索")

# 处理按钮点击事件
if search_button:
    matched_idioms = match_idioms(user_input, idioms_list)
    if matched_idioms:
        st.write("匹配到的成语：")
        for idiom in matched_idioms:
            st.write(idiom)
    else:
        st.write("未找到匹配的成语")
