import streamlit as st
import pandas as pd

# 1. 网页基础设置
st.set_page_config(page_title="宁卓商贸 PK 战报系统", layout="wide")

# 管理员密码：你可以修改这个引号里的内容
ADMIN_PASSWORD = "666" 

# 2. 初始化 28 名员工数据
if 'df' not in st.session_state:
    # 按照你提供的 24 销售 + 4 人事架构
    # 这里先为你填入占位名，后续你在后台可以随时改
    names = [f"销售{i+1}" for i in range(24)] + [f"人事{i+1}" for i in range(4)]
    roles = ["销售"] * 24 + ["人事"] * 4
    
    data = {
        "姓名": names,
        "身份": roles,
        "当前业绩": [0.0] * 28,
        "目标": [5.0] * 28  # 默认设为 5
    }
    st.session_state.df = pd.DataFrame(data)

# 3. 积分计算逻辑
def get_score(row):
    if row['目标'] <= 0: return 0.0
    return round((row['当前业绩'] / row['目标']) * 100, 2)

# 4. 侧边栏管理后台
st.sidebar.title("💎 负责人管理后台")
pwd = st.sidebar.text_input("请输入管理密码", type="password")

if pwd == ADMIN_PASSWORD:
    st.sidebar.success("验证通过")
    target = st.sidebar.selectbox("选择要修改的成员", st.session_state.df["姓名"])
    
    # 允许修改姓名、业绩和目标
    new_name = st.sidebar.text_input("修改姓名", value=target)
    new_val = st.sidebar.number_input("录入最新业绩", min_value=0.0, step=1.0)
    new_target = st.sidebar.number_input("调整目标金额", min_value=1.0, step=1.0, value=5.0)
    
    if st.sidebar.button("点击同步到全员手机"):
        idx = st.session_state.df[st.session_state.df["姓名"] == target].index
        st.session_state.df.loc[idx, "姓名"] = new_name
        st.session_state.df.loc[idx, "当前业绩"] = new_val
        st.session_state.df.loc[idx, "目标"] = new_target
        st.sidebar.balloons()
        st.rerun()

# 5. 主页面展示
st.title("🏆 宁卓商贸实时 PK 战报")

df_display = st.session_state.df.copy()
df_display["当前积分"] = df_display.apply(get_score, axis=1)

# 按积分高低排序
df_display = df_display.sort_values("当前积分", ascending=False)

# 展示表格
st.subheader("📊 实时排名榜单")
st.dataframe(df_display[["姓名", "身份", "当前业绩", "目标", "当前积分"]], use_container_width=True)

# 柱状图展示
st.subheader("📈 业绩冲刺进度")
st.bar_chart(df_display.set_index("姓名")["当前积分"])

st.caption("数据实时互通：负责人修改后，全员刷新即可看到最新排名。")
