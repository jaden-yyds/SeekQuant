import time

import streamlit as st
from streamlit_option_menu import option_menu
import tools
from chatbot import async_send_message, async_chat_split_think_answer, print_events, llm

assistants = [
    {"label": "李园园（需求）", "value": "lyy", "icon": "book", "key": "lyy", "image": "static/lyy_avatar.png",
     "model": "DeepSeek-R1-671B", "greet": "你好！我是AI助手李园园（基于DeepSeek-R1-671B微调训练）很高兴为你解答需求相关的问题。"},
    {"label": "罗灯杰（开发）", "value": "jaden", "icon": "android", "key": "jaden", "image": "static/jaden_avatar.png",
     "model": "DeepSeek-Coder-V2-236B", "greet": "你好！我是AI助手罗灯杰（基于DeepSeek-Coder-V2-236B微调训练）致力于帮助你解决任何代码相关的问题。"},
    {"label": "陈鹏辉（测试）", "value": "cph", "icon": "bug", "key": "cph", "image": "static/cph_avatar.png",
     "model": "DeepSeek-LLM-67B", "greet": "你好！我是AI助手陈鹏辉（基于DeepSeek-LLM-67B）能够与您畅聊娱乐八卦、新闻体育、金融科技等内容。"}
]
assistant_names = [item["label"] for item in assistants]
st.set_page_config(page_title="SeekQuant", page_icon=":cn:")
with st.sidebar:
    assistant_selected = option_menu("模型选择", menu_icon="star",
                           options=assistant_names,
                           icons=[item["icon"] for item in assistants], default_index=1)
    active_avatar = assistants[assistant_names.index(assistant_selected)]["image"]
    active_model = assistants[assistant_names.index(assistant_selected)]["model"]
    active_greet = assistants[assistant_names.index(assistant_selected)]["greet"]
    st.logo(image=f"static/{active_model}.png", size="large", link=None, icon_image=active_avatar)

def main():

    question = st.chat_input("Say something")
    if assistant_selected:
        st.chat_message("assistant", avatar=active_avatar).write(active_greet)
    if question:
        with st.chat_message("user"):
            st.write(question)
        with st.chat_message("assistant", avatar=active_avatar):
            # 获取分离后的双流
            result_stream = llm.astream(question)
            thinking_stream, answer_stream = tools.split_async_generator(result_stream)
            # 并行消费两个流
            with st.status("思考中...", expanded=True) as thinking_status:
                thinking_start_time = time.perf_counter()  # 记录开始时间
                st.write_stream(thinking_stream)
                thinking_end_time = time.perf_counter()
                thinking_status.update(
                    label=f"已深度思考{thinking_end_time - thinking_start_time:.2f}秒", state="complete", expanded=True
                )
            st.write_stream(answer_stream)

if __name__ == "__main__":
    # asyncio.run(main())
    main()