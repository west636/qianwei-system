import streamlit as st
import random
import time

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
if "welcome_printed" not in st.session_state:
    st.session_state.welcome_printed = True
    st.session_state.terminal_output.append('你好，欢迎使用千维系统。')

# 机制状态
if "cmd_use_times" not in st.session_state:
    st.session_state.cmd_use_times = 0
if "martin_warning" not in st.session_state:
    st.session_state.martin_warning = False
if "system_destroyed" not in st.session_state:
    st.session_state.system_destroyed = False
if "warning_added" not in st.session_state:
    st.session_state.warning_added = False
if "enter_confirm" not in st.session_state:
    st.session_state.enter_confirm = False
if "pw_countdown_started" not in st.session_state:
    st.session_state.pw_countdown_started = False # 标记密码失败倒计时是否已经启动

def print_term(text):
    st.session_state.terminal_output.append(text)

terminal = st.empty()
def render_terminal():
    terminal.code("\n".join(st.session_state.terminal_output), language="text")

render_terminal()

# ========== 密码输入阶段 ==========
if not st.session_state.logged_in and not st.session_state.system_destroyed:
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
        # 密码机会耗尽，启动带1秒间隔的倒计时
        if not st.session_state.pw_countdown_started:
            print_term('警告：检测到外部访问尝试。来源：未知。建议终止当前操作。系统将在10秒后关闭。')
            st.session_state.pw_countdown_started = True
            render_terminal()
            # 10秒倒计时，每秒刷新
            for i in range(10, 0, -1):
                time.sleep(1)
                print_term(f"倒计时：{i}...")
                render_terminal()
            time.sleep(1)
            print_term("系统已关闭。")
            render_terminal()

# ========== 指令交互阶段 ==========
if st.session_state.logged_in and not st.session_state.system_destroyed:
    if st.session_state.martin_warning:
        if not st.session_state.warning_added:
            print_term("⚠️ 严重警告！检测反向追踪信号！")
            print_term("⚠️ 警告：正在被人接入！检测到外部反向追踪，是否继续使用？")
            st.session_state.warning_added = True

        if not st.session_state.enter_confirm:
            col1, col2 = st.columns(2)
            with col1:
                btn_stop = st.button("立刻停止使用")
            with col2:
                btn_continue = st.button("继续使用")

            if btn_stop:
                print_term("已断开连接。千维系统暂时不可用，本次追踪终止。")
                st.session_state.logged_in = False
                st.session_state.martin_warning = False
                st.session_state.warning_added = False
                st.rerun()

            if btn_continue:
                print_term('系统传出一阵男声，很明显不是系统自带的：“我抓到你了。”')
                print_term('系统提示：发现系统被修改，是否启动备用计划。')
                st.session_state.enter_confirm = True
                st.rerun()
        else:
            with st.form("confirm_form"):
                ans = st.text_input("是否启动备用计划？请输入 是 / 否", key="ans_input")
                btn_ok = st.form_submit_button("确认")

            if btn_ok:
                ans_clean = ans.strip()
                if ans_clean == "是":
                    print_term("启动备用计划，开始销毁全部测试系统数据。")
                    render_terminal()
                    # 销毁倒计时，每秒一行
                    for i in range(5, 0, -1):
                        time.sleep(1)
                        print_term(f"倒计时：{i}...")
                        render_terminal()

                    intercept_roll = random.randint(1, 100)
                    if intercept_roll <= 50:
                        print_term("【错误】销毁指令被外部入侵行为拦截！系统保留，但追踪链路仍存在风险。")
                        st.session_state.logged_in = False
                        st.session_state.martin_warning = False
                        st.session_state.warning_added = False
                        st.session_state.enter_confirm = False
                    else:
                        print_term("销毁完成。核心系统正在上传，删除测试系统28743，启动测试系统28744，千维系统正在关闭。")
                        print_term("系统已上传至未知地址，后续接入只会得到空响应。")
                        st.session_state.system_destroyed = True
                    st.rerun()
                elif ans_clean == "否":
                    print_term("放弃启动备用计划。连接紧急切断，追踪链路中断。")
                    st.session_state.logged_in = False
                    st.session_state.martin_warning = False
                    st.session_state.warning_added = False
                    st.session_state.enter_confirm = False
                    st.rerun()

    else:
        def submit_cmd():
            cmd_raw = st.session_state.cmd_input
            if not cmd_raw:
                return
            cmd = cmd_raw.strip()
            st.session_state.cmd_use_times += 1
            use_times = st.session_state.cmd_use_times
            expose_rate = min(use_times * 10, 50)

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

            roll = random.randint(1, 100)
            if roll <= expose_rate:
                st.session_state.martin_warning = True
                st.session_state.warning_added = False
                st.session_state.enter_confirm = False

            st.session_state.cmd_input = ""
            st.rerun()

        prompt_text = '可进行电力，水力，政府警戒，监控系统，通讯系统（请输入电力/水力/政府/监控/通讯），或输入“结束”以结束操作：'
        st.text_input(prompt_text, key="cmd_input", on_change=submit_cmd)

if st.session_state.system_destroyed:
    print_term("\n【系统永久关闭】千维测试系统已销毁，无法继续使用。")

render_terminal()


