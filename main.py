import os
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


# 获取期望的登录凭证（可通过环境变量覆盖，默认 admin/admin）
def expected_credentials():
    username = os.getenv("APP_USERNAME", "admin")
    password = os.getenv("APP_PASSWORD", "admin")
    return username, password


# 登录页
def render_login_page():
    st.title("登录")

    with st.form("login_form"):
        username = st.text_input("用户名")
        password = st.text_input("密码", type="password")
        submitted = st.form_submit_button("登录")

    if submitted:
        exp_user, exp_pwd = expected_credentials()
        if username == exp_user and password == exp_pwd:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("登录成功")
        else:
            st.error("用户名或密码错误")

    st.caption("默认账户：admin / admin（可通过环境变量 APP_USERNAME 与 APP_PASSWORD 配置）")


def render_logout_sidebar():
    with st.sidebar:
        st.write(f"当前用户：{st.session_state.get('username', '未登录')}")
        if st.button("退出登录"):
            st.session_state.clear()
            if hasattr(st, "rerun"):
                st.rerun()
            elif hasattr(st, "experimental_rerun"):
                st.experimental_rerun()


# 登录拦截：未登录则只展示登录页
if not st.session_state.get("authenticated", False):
    render_login_page()
    st.stop()

# 通过登录后显示主页面
render_logout_sidebar()

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
