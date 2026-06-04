import streamlit as st
import pandas as pd

# 1. 页面基本设置
st.set_page_config(page_title="流量点击查询", layout="wide")

st.subheader("流量点击查询")


# 2. 模拟加载数据
@st.cache_data
def load_data():
    return pd.DataFrame({
        '日期': [
            '2026.03.09', '2026.03.09', '2026.03.10', '2026.03.10', '2026.03.10',
            '2026.03.11', '2026.03.11', '2026.03.11', '2026.03.12', '2026.03.12'
        ],
        '时间': [
            '07:43', '14:20', '09:15', '16:30', '19:50',
            '10:53', '11:15', '15:10', '08:05', '22:45'
        ],
        '商家名称': ['中国人民财产保险股份有限公司'] * 10,
        '引流推送平台': ['交易猫官网、APP'] * 10,
        '推送内容': ['平台产品展示页曝光量'] * 10,
        '用户ID': [
            '25053*********52', '83921*********14', '11024*********76', '54390*********33', '74209*********88',
            '31111*********62', '99201*********45', '69809*********02', '45102*********91', '22019*********08'
        ],
        '链接': ['https://m.jiaoyimao.com/'] * 10
    })


df = load_data()

# 3. 构建顶部查询表单
with st.form("search_form"):
    st.write("费用账单 / 流量明细")

    col1, col2, col3 = st.columns(3)
    with col1:
        search_date = st.date_input("账单日期区间", value=())
    with col2:
        # 位置互换：这里换成 时间
        search_time = st.text_input("时间 (如 15:10)")
    with col3:
        # 位置互换：这里换成 商家名称 / 用户ID
        search_id = st.text_input("商家名称 / 用户ID")

    btn_col1, btn_empty, btn_col2 = st.columns([1, 8, 1])
    with btn_col1:
        submit_button = st.form_submit_button(label='查询', use_container_width=True)
    with btn_col2:
        download_button = st.form_submit_button(label='下载', use_container_width=True)

# 4. 逻辑处理：点击查询后过滤数据
filtered_df = df.copy()

if submit_button:
    if search_id:
        mask = filtered_df['用户ID'].str.contains(search_id, na=False) | filtered_df['商家名称'].str.contains(search_id,
                                                                                                              na=False)
        filtered_df = filtered_df[mask]

    if search_time:
        filtered_df = filtered_df[filtered_df['时间'].str.contains(search_time, na=False)]

    if search_date and len(search_date) == 2:
        start_date, end_date = search_date
        df_dates = pd.to_datetime(filtered_df['日期'], format='%Y.%m.%d').dt.date
        date_mask = (df_dates >= start_date) & (df_dates <= end_date)
        filtered_df = filtered_df[date_mask]

# 5. 展示结果表格
st.subheader("流量点击明细列表")

st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "链接": st.column_config.LinkColumn("展示页链接", display_text="点击查看曝光页面")
    }
)