import streamlit as st
import time
import random

# 页面基础配置
st.set_page_config(page_title="千维系统", layout="wide")

# 终端黑底绿字样式
st.markdown("""
<style>
.main {background-color:#000000;}
.stApp {background-color:#000000; color:#39ff14; font-family:Consolas,monospace; font-size:16px;}
.stTextInput>div>div>input {background:#111111; color:#39ff14; border:1px solid #39ff14;}
.stButton>button {background:#111111; color:#39ff14; border:1px solid #39ff14;}
</style>
""", unsafe_allow_html=True)

# ========== 会话状态初始化 ==========
if "count" not in st.session_state:
    st.session_state.count = 0
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "terminal_output" not in st.session_state:
    st.session_state.terminal_output = []
if "countdown_running" not in st.session_state:
    st.session_state.countdown_running = False
if "welcome_printed" not in st.session_state:
    st.session_state.welcome_printed = True
    st.session_state.terminal_output.append('你好，欢迎使用千维系统。')

# 机制状态
if "cmd_use_times" not in st.session_state:
    st.session_state.cmd_use_times = 0  # 指令使用次数，决定暴露概率
if "called_8764239" not in st.session_state:
    st.session_state.called_8764239 = True # 默认已经监听过8764239，马丁追踪风险一直生效
if "martin_warning" not in st.session_state:
    st.session_state.martin_warning = False # 是否触发马丁警告
if "system_destroyed" not in st.session_state:
    st.session_state.system_destroyed = False # 是否系统被销毁

def print_term(text):
    st.session_state.terminal_output.append(text)

terminal = st.empty()
def render_terminal():
    terminal.code("\n".join(st.session_state.terminal_output), language="text")

render_terminal()

# ========== 密码输入阶段 ==========
if not st.session_state.logged_in and not st.session_state.countdown_running and not st.session_state.system_destroyed:
    if st.session_state.count < 10:
        def submit_pwd():
            pwd_raw = st.session_state.pwd_input
            if not pwd_raw:
                return
            try:
                pws = int(pwd_raw)
                if pws == 54816871:
                    print_term('千维系统已连线，测试版本29743，测试代号卢奇菲罗，请下达指令。')
                    st.session_state.logged_in = True
                else:
                    st.session_state.count += 1
                    remain = 10 - st.session_state.count
                    print_term(f'密码错误，你还有 {remain} 次机会。')
            except ValueError:
                print_term("密码必须是数字！")
            st.session_state.pwd_input = ""

        st.text_input('请输入密码：', key="pwd_input", on_change=submit_pwd)

    else:
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
if st.session_state.logged_in and not st.session_state.system_destroyed:
    # 触发马丁警告，进入分支选择
    if st.session_state.martin_warning:
        print_term("⚠️ 警告：正在被人接入！检测到外部反向追踪，是否继续使用？")
        opt1, opt2 = st.columns(2)
        with opt1:
            if st.button("立刻停止使用"):
                print_term("已断开连接。千维系统暂时不可用，本次追踪终止。")
                st.session_state.logged_in = False
                st.session_state.martin_warning = False
                st.rerun()
        with opt2:
            if st.button("继续使用"):
                print_term('【通讯接入】男性声音："我抓到你了。"')
                time.sleep(1.2)
                print_term('【系统提示】切换备用信道，女声：发现系统被修改，是否启动备用计划。')
                ans = st.text_input("请输入 是 / 否", key="martin_answer")
                if ans:
                    if ans.strip() == "是":
                        print_term("核心系统正在上传，删除测试系统28743，启动测试系统28744，千维系统正在关闭。")
                        print_term("系统已上传至未知地址，后续拨打号码只会听到忙音。马丁·琴将会展开袭击。")
                        st.session_state.system_destroyed = True
                    else:
                        print_term("拒绝启用备用计划。连接紧急切断，追踪链路中断。")
                        st.session_state.logged_in = False
                        st.session_state.martin_warning = False
                    st.rerun()

    else:
        def submit_cmd():
            cmd_raw = st.session_state.cmd_input
            if not cmd_raw:
                return
            cmd = cmd_raw.strip()
            st.session_state.cmd_use_times += 1
            use_times = st.session_state.cmd_use_times
            # 暴露概率：第N次=N*10%，上限50%，不再打印概率提示
            expose_rate = min(use_times * 10, 50)

            # 指令执行
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
                st.session_state.logged_in = False
                st.session_state.cmd_input = ""
                st.rerun()
                return
            else:
                print_term('无效指令。')

            # 暴露判定（默认已经打过8764239，每次都roll）
            roll = random.randint(1,100)
            if roll <= expose_rate:
                print_term("\n⚠️ 严重警告！检测反向追踪信号！马丁·琴正在接入！")
                st.session_state.martin_warning = True

            st.session_state.cmd_input = ""
            st.rerun()

        prompt_text = '可进行电力，水力，政府警戒，监控系统，通讯系统（请输入电力/水力/政府/监控/通讯），或输入“结束”以结束操作：'
        st.text_input(prompt_text, key="cmd_input", on_change=submit_cmd)

# 系统销毁后提示
if st.session_state.system_destroyed:
    print_term("\n【系统永久关闭】千维测试系统已销毁，无法继续使用。")

render_terminal()

# 重置按钮
if st.button("🔄 重置系统（清空记录，重新开始）"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.rerun()
