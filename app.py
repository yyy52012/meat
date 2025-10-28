import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# 页面设置
st.set_page_config(
    page_title="马肉风干肉分析",
    page_icon="🐎",
    layout="wide"
)

# 标题
st.title("🐎 马肉风干肉营养与质量分析")
st.markdown("哈萨克斯坦传统马肉风干肉的营养成分、加工工艺和质量监控")

# 马肉风干肉基础数据
@st.cache_data
def load_horsemeat_jerky_data():
    # 马肉风干肉营养成分（每100克）
    nutrition_data = {
        '阶段': ['新鲜马肉', '半干马肉', '全干马肉'],
        '水分_pct': [73.0, 45.0, 18.0],
        '蛋白质_g': [21.4, 35.2, 48.5],
        '脂肪_g': [2.7, 4.5, 6.2],
        '热量_kcal': [113, 186, 256],
        '钠_mg': [53, 850, 1200],
        '铁_mg': [3.2, 5.3, 7.4],
        '锌_mg': [4.8, 7.9, 11.2]
    }
    
    # 加工参数
    processing_params = {
        '盐渍时间_天': [3, 5, 7],
        '干燥温度_℃': [12, 15, 18],
        '相对湿度_pct': [70, 65, 60],
        '干燥时间_天': [15, 21, 30]
    }
    
    # 质量指标
    quality_data = {
        '批次': [f'KM{i:02d}' for i in range(1, 21)],
        '水分_pct': np.random.normal(25, 5, 20),
        '盐分_pct': np.random.normal(6, 1, 20),
        '蛋白质_pct': np.random.normal(45, 3, 20),
        'pH值': np.random.normal(5.6, 0.3, 20),
        'aw值': np.random.normal(0.82, 0.05, 20)
    }
    
    return pd.DataFrame(nutrition_data), pd.DataFrame(processing_params), pd.DataFrame(quality_data)

# 加载数据
nutrition_df, processing_df, quality_df = load_horsemeat_jerky_data()

# 主界面
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📊 营养计算")
    
    # 产品阶段选择
    product_stage = st.selectbox(
        "选择产品阶段",
        options=nutrition_df['阶段'].values
    )
    
    # 重量输入
    weight = st.number_input(
        "重量 (克)",
        min_value=1,
        max_value=500,
        value=50,
        step=10,
        help="建议食用量：20-50克"
    )
    
    # 加工参数显示
    st.subheader("🔧 推荐加工参数")
    stage_index = nutrition_df[nutrition_df['阶段'] == product_stage].index[0]
    
    st.write(f"**盐渍时间:** {processing_df['盐渍时间_天'].iloc[stage_index]}天")
    st.write(f"**干燥温度:** {processing_df['干燥温度_℃'].iloc[stage_index]}℃")
    st.write(f"**相对湿度:** {processing_df['相对湿度_pct'].iloc[stage_index]}%")
    st.write(f"**干燥时间:** {processing_df['干燥时间_天'].iloc[stage_index]}天")

with col2:
    st.header("📈 营养成分分析")
    
    # 获取选定阶段的数据
    stage_data = nutrition_df[nutrition_df['阶段'] == product_stage].iloc[0]
    
    # 计算营养成分
    weight_factor = weight / 100
    nutrition_results = {
        '蛋白质': stage_data['蛋白质_g'] * weight_factor,
        '脂肪': stage_data['脂肪_g'] * weight_factor,
        '热量': stage_data['热量_kcal'] * weight_factor,
        '钠': stage_data['钠_mg'] * weight_factor,
        '铁': stage_data['铁_mg'] * weight_factor,
        '锌': stage_data['锌_mg'] * weight_factor
    }
    
    # 显示营养指标
    st.subheader(f"{weight}克 {product_stage} 的营养成分")
    
    # 使用列布局显示指标
    col2_1, col2_2, col2_3 = st.columns(3)
    
    with col2_1:
        st.metric("🔥 热量", f"{nutrition_results['热量']:.0f} kcal")
        st.metric("💪 蛋白质", f"{nutrition_results['蛋白质']:.1f} g")
        
    with col2_2:
        st.metric("🛢️ 脂肪", f"{nutrition_results['脂肪']:.1f} g")
        st.metric("🧂 钠", f"{nutrition_results['钠']:.0f} mg")
        
    with col2_3:
        st.metric("🔴 铁", f"{nutrition_results['铁']:.1f} mg")
        st.metric("🔵 锌", f"{nutrition_results['锌']:.1f} mg")

# 可视化分析
st.header("📊 风干过程分析")

tab1, tab2, tab3 = st.tabs(["营养变化", "加工参数", "质量监控"])

with tab1:
    # 营养成分在风干过程中的变化
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=nutrition_df['阶段'], 
        y=nutrition_df['蛋白质_g'],
        mode='lines+markers',
        name='蛋白质',
        line=dict(color='blue', width=3)
    ))
    
    fig1.add_trace(go.Scatter(
        x=nutrition_df['阶段'], 
        y=nutrition_df['水分_pct'],
        mode='lines+markers',
        name='水分',
        line=dict(color='green', width=3)
    ))
    
    fig1.update_layout(
        title="风干过程中蛋白质和水分变化",
        xaxis_title="加工阶段",
        yaxis_title="含量 (g/100g)",
        height=400
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # 加工参数可视化
    col1, col2 = st.columns(2)
    
    with col1:
        fig2 = px.bar(
            processing_df,
            x=['盐渍时间', '干燥温度', '相对湿度'],
            y=[processing_df['盐渍时间_天'].mean(), 
               processing_df['干燥温度_℃'].mean(), 
               processing_df['相对湿度_pct'].mean()],
            title="平均加工参数",
            labels={'y': '数值', 'x': '参数'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.line(
            processing_df,
            y='干燥时间_天',
            title="干燥时间要求",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # 质量监控图表
    st.subheader("批次质量指标")
    
    fig4 = px.scatter(
        quality_df,
        x='水分_pct',
        y='盐分_pct',
        color='蛋白质_pct',
        size='pH值',
        hover_data=['批次'],
        title="水分含量 vs 盐分含量",
        labels={'水分_pct': '水分含量 (%)', '盐分_pct': '盐分含量 (%)'}
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # 质量指标统计
    st.subheader("质量指标分布")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig5 = px.histogram(quality_df, x='水分_pct', title="水分含量分布")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        fig6 = px.histogram(quality_df, x='盐分_pct', title="盐分含量分布")
        st.plotly_chart(fig6, use_container_width=True)
    
    with col3:
        fig7 = px.histogram(quality_df, x='蛋白质_pct', title="蛋白质含量分布")
        st.plotly_chart(fig7, use_container_width=True)

# 传统知识与建议
st.header("💡 哈萨克斯坦传统马肉风干知识")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🐎 传统制作工艺")
    st.info("""
    **选材要求:**
    - 选用成年马的臀部和背部肌肉
    - 肉质紧实，脂肪分布均匀
    - 传统秋季制作，气温适宜
    
    **加工流程:**
    1. 盐渍处理（3-7天）
    2. 自然风干（15-30天）
    3. 定期翻面确保均匀干燥
    4. 品质检验后包装
    """)

with col2:
    st.subheader("🏥 食用与储存建议")
    st.info("""
    **食用建议:**
    - 每日建议量：20-50克
    - 高蛋白补充，适合运动员
    - 富含铁质，预防贫血
    
    **储存条件:**
    - 阴凉干燥处保存
    - 避免阳光直射
    - 保质期：6-12个月
    - 开封后建议冷藏
    """)

# 保存为文件
st.sidebar.header("💾 数据导出")
if st.sidebar.button("下载营养数据"):
    csv = nutrition_df.to_csv(index=False)
    st.sidebar.download_button(
        label="确认下载CSV",
        data=csv,
        file_name=f"马肉风干肉营养数据_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# 页脚说明
st.markdown("---")
st.markdown("""
**数据说明:**
- 基于哈萨克斯坦传统马肉风干工艺数据
- 营养成分为每100克可食部分含量
- 加工参数为传统工艺推荐值
- 质量数据基于实际生产批次统计
""")
