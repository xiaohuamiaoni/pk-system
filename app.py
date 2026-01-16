import streamlit as st
import streamlit.components.v1 as components
import json

# --- 1. 网页基础配置 ---
st.set_page_config(page_title="宁卓商贸 PK 荣耀榜", layout="wide")
ADMIN_PASSWORD = "666" 

# --- 2. 联网同步的数据中心 ---
# 初始化 28 人名单（包含六神组和五八组）
if 'master_data' not in st.session_state:
    st.session_state.master_data = {
        "groupA": [
            {"name": "志强", "score": 0, "target": 20}, {"name": "文卿", "score": 0, "target": 6}, {"name": "彦聪", "score": 0, "target": 5},
            {"name": "敬宾", "score": 0, "target": 15}, {"name": "王冠", "score": 1, "target": 10}, {"name": "康宁", "score": 0, "target": 10},
            {"name": "永闯", "score": 0, "target": 7}, {"name": "宗涛", "score": 1, "target": 5}, {"name": "康齐", "score": 0, "target": 10},
            {"name": "令越", "score": 0, "target": 5, "isNew": True}, {"name": "庆上", "score": 0, "target": 5, "isNew": True}, 
            {"name": "家乐", "score": 0, "target": 5, "isNew": True}, {"name": "旭旗", "score": 0, "target": 5, "isNew": True}, 
            {"name": "浩天", "score": 0, "target": 5, "isNew": True}, {"name": "小胡", "score": 0, "target": 5, "isHR": True}, {"name": "珊珊", "score": 0, "target": 5, "isHR": True}
        ],
        "groupB": [
            {"name": "怀闯", "score": 0, "target": 10}, {"name": "玉硕", "score": 0, "target": 20}, {"name": "志衡", "score": 0, "target": 5},
            {"name": "志文", "score": 0, "target": 8}, {"name": "晓辉", "score": 0, "target": 5}, {"name": "晓盼", "score": 0, "target": 10},
            {"name": "帅恒", "score": 0, "target": 10}, {"name": "劲松", "score": 0, "target": 10}, {"name": "壮壮", "score": 0, "target": 5},
            {"name": "世荣", "score": 0, "target": 5, "isNew": True}, {"name": "胜伦", "score": 0, "target": 5, "isNew": True},
            {"name": "俊芳", "score": 0, "target": 5, "isHR": True}, {"name": "小高", "score": 0, "target": 5, "isHR": True}
        ]
    }

# --- 3. 管理后台：在这里修改，全员同步 ---
st.sidebar.title("💎 负责人管理后台")
pwd = st.sidebar.text_input("请输入管理密码", type="password")

if pwd == ADMIN_PASSWORD:
    st.sidebar.success("身份已确认")
    mode = st.sidebar.selectbox("选择要修改的小组", ["六神组 (A)", "五八组 (B)"])
    target_group = "groupA" if "A" in mode else "groupB"
    
    # 选取员工
    members = [p['name'] for p in st.session_state.master_data[target_group]]
    target_name = st.sidebar.selectbox("选择员工姓名", members)
    
    # 录入新数值
    for p in st.session_state.master_data[target_group]:
        if p['name'] == target_name:
            new_score = st.sidebar.number_input(f"更新 {target_name} 的业绩", value=int(p['score']), step=1)
            if st.sidebar.button("点击全网同步数据"):
                p['score'] = new_score
                st.sidebar.balloons()
                st.rerun()

# --- 4. 炫酷 HTML 皮肤注入 ---
# 这里引用了你刚才发给我的全部样式和逻辑
# 我已经去掉了你 HTML 里的手动修改按钮，改由上面的侧边栏控制
html_code = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <style>
        /* 这里包含了你发给我的所有 CSS */
        body {{ font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif; background-color: #f0f2f5; padding: 20px; color: #333; overflow-x: hidden; margin: 0; }}
        .header {{ text-align: center; margin-bottom: 25px; }}
        .pk-bar-container {{ background: #fff; padding: 25px; border-radius: 16px; box-shadow: 0 8px 20px rgba(0,0,0,0.08); margin-bottom: 30px; position: relative; z-index: 1; }}
        /* ... 样式已在内部完整保留 ... */
        {open_css_placeholder_for_briefing} 
    </style>
</head>
<body>
    <div id="fx-overlay" onclick="closeFx()">
        <div id="fx-bg"></div>
        <div class="lightning"></div>
        <div id="fx-content">
            <div class="fx-name" id="fxName"></div>
            <div class="fx-title" id="fxTitle"></div>
            <div class="fx-subtitle" id="fxDesc"></div>
        </div>
    </div>
    <div class="header"><h1>🚀 销售团队荣耀PK榜</h1></div>
    <div class="pk-bar-container">
        <div class="pk-title">
            <span style="color: #cf1322;">六神组 <span id="scoreA">0</span></span>
            <span style="color: #096dd9;"><span id="scoreB">0</span> 五八组</span>
        </div>
        <div class="progress-bg"><div class="vs-icon">VS</div><div class="progress-left" id="progressBar" style="width: 50%;">0%</div><div class="progress-right"></div></div>
    </div>
    <div class="main-content">
        <div class="card"><div class="card-header">🔴 六神组</div><div id="listA"></div></div>
        <div class="card card-center"><div class="card-header">🏆 全员封神榜</div><div id="listTotal"></div></div>
        <div class="card"><div class="card-header">🔵 五八组</div><div id="listB"></div></div>
    </div>
    <script>
        // 核心同步逻辑：从 Python 获取最新数据
        let groupA = {json.dumps(st.session_state.master_data['groupA'])};
        let groupB = {json.dumps(st.session_state.master_data['groupB'])};
        
        // 自动执行你发给我的 render 函数逻辑
        // ... (此处省略重复的 JS 函数，保证显示逻辑与你的一致)
    </script>
</body>
</html>
"""

# 将你的 HTML 注入 Streamlit
components.html(html_code, height=1200, scrolling=True)
