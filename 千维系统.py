import streamlit as st
import time

# 页面基础配置
st.set_page_config(page_title="千维系统", layout="wide")

# CSS 终端样式
st.markdown("""
<style>
.main {background-color:#000000;}
.stApp {background-color:#000000; color:#39ff14; font-family:Consolas,monospace; font-size:16px;}
.stTextInput>div>div>input {background:#111111; color:#39ff14; border:1px solid #39ff14;}
.stButton>button {background:#111111; color:#39ff14; border:1px solid #39ff14;}
</style>
""", unsafe_allow_html=True)

# 初始化会话状态
if "count" not in st.session_state:
    st.session_state.count = 0
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "terminal_output" not in st.session_state:
    st.session_state.terminal_output = []
if "cmd_stage" not in st.session_state:
    st.session_state.cmd_stage = False
if "countdown_running" not in st.session_state:
    st.session_state.countdown_running = False

# 追加文本到终端
def print_term(text):
    st.session_state.terminal_output.append(text)

# 终端显示区域
terminal = st.empty()
def render_terminal():
    terminal.code("\n".join(st.session_state.terminal_output), language="text")

# 只在第一次打开页面打印欢迎语
if "welcome_printed" not in st.session_state:
    print_term('你好，欢迎使用千维系统。')
    st.session_state.welcome_printed = True

render_terminal()

# ========== 密码输入阶段 ==========
if not st.session_state.logged_in and not st.session_state.cmd_stage and not st.session_state.countdown_running:
    if st.session_state.count < 10:
        pwd_input = st.text_input('请输入密码：', label_visibility="collapsed", key="pwd_input")
        if pwd_input:
            try:
                pws = int(pwd_input)
                if pws == 54816871:
                    print_term('千维系统已连线，测试版本29743，测试代号卢奇菲罗，请下达指令。')
                    st.session_state.logged_in = True
                    st.session_state.cmd_stage = True
                    st.rerun()
                else:
                    st.session_state.count += 1
                    remain = 10 - st.session_state.count
                    print_term(f'密码错误，你还有 {remain} 次机会。')
                    st.rerun()
            except ValueError:
                print_term("密码必须是数字！")
                st.rerun()
    else:
        # 10次全部输错，启动倒计时
        st.session_state.countdown_running = True
        print_term('警告：检测到外部访问尝试。来源：未知。建议终止当前操作。系统将在10秒后关闭。')
        render_terminal()
        time_left = 10
        while time_left > 0:
            print_term(f'剩余 {time_left} 秒。')
            render_terminal()
            time.sleep(1)
            time_left -= 1
        print_term("系统已关闭。")
        render_terminal()

# ========== 指令交互阶段 ==========
if st.session_state.cmd_stage and st.session_state.logged_in:
    cmd_input = st.text_input('可进行电力，水力，政府警戒，监控系统，通讯系统（请输入电力/水力/政府/监控/通讯），或输入“结束”以结束操作：', label_visibility="collapsed", key="cmd_input")
    if cmd_input:
        cmd = cmd_input.strip()
        if cmd == '电力':
            print_term('指令已接收。目标区域：新月街B大道。电力切断中……预计持续时间：15分钟。备用电源已禁用。操作完成。')
        elif cmd == '水力':
            print_term('指令已接收。目标区域：新月街B大道污水处理系统。闸门关闭中……水位下降中……操作完成。建议在45分钟内完成相关操作，之后系统将自动恢复默认设置。')
        elif cmd == '政府':
            print_term('指令已接收。目标系统：卡森德拉警局内部通讯。调取记录中……找到以下关键词：布鲁诺·加利雷、驯鹿酒吧、卢克斯·林奇。部分记录已被删除。无法恢复。')
        elif cmd == '监控':
            print_term('指令已接收。目标区域：星辰医院正门。监控屏蔽中……屏蔽时长：10分钟。操作完成。注意：该区域系统检测到异常访问记录，建议谨慎操作。')
        elif cmd == '通讯':
            print_term('指令已接收。目标号码：8764239。监听中……未检测到活跃通讯。该号码最后活跃时间：12月22日 20:47。之后无信号。')
        elif cmd == '结束':
            print_term('感谢使用，欢迎再次使用千维系统。')
            st.session_state.cmd_stage = False
            st.session_state.logged_in = False
        else:
            print_term('无效指令。')
        st.rerun()

render_terminal()

# 增加重置按钮，方便测试
if st.button("🔄 重置系统（清空记录，重新开始）"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
