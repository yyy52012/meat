import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Настройки страницы
st.set_page_config(
    page_title="Анализ вяленой конины",
    page_icon="🐎",
    layout="wide"
)

# Заголовок
st.title("🐎 Анализ питательности и качества вяленой конины")
st.markdown("Пищевая ценность, технология обработки и контроль качества традиционной казахской вяленой конины")

# Базовые данные вяленой конины
@st.cache_data
def load_horsemeat_jerky_data():
    # Пищевая ценность вяленой конины (на 100 г)
    nutrition_data = {
        'Этап': ['Свежая конина', 'Полувяленая конина', 'Полностью вяленая конина'],
        'Влага_%': [73.0, 45.0, 18.0],
        'Белки_г': [21.4, 35.2, 48.5],
        'Жиры_г': [2.7, 4.5, 6.2],
        'Калории_ккал': [113, 186, 256],
        'Натрий_мг': [53, 850, 1200],
        'Железо_мг': [3.2, 5.3, 7.4],
        'Цинк_мг': [4.8, 7.9, 11.2]
    }
    
    # Параметры обработки
    processing_params = {
        'Время_засолки_дни': [3, 5, 7],
        'Температура_сушки_℃': [12, 15, 18],
        'Относительная_влажность_%': [70, 65, 60],
        'Время_сушки_дни': [15, 21, 30]
    }
    
    # Показатели качества
    quality_data = {
        'Партия': [f'KM{i:02d}' for i in range(1, 21)],
        'Влага_%': np.random.normal(25, 5, 20),
        'Соль_%': np.random.normal(6, 1, 20),
        'Белки_%': np.random.normal(45, 3, 20),
        'pH': np.random.normal(5.6, 0.3, 20),
        'aw': np.random.normal(0.82, 0.05, 20)
    }
    
    return pd.DataFrame(nutrition_data), pd.DataFrame(processing_params), pd.DataFrame(quality_data)

# Загрузка данных
nutrition_df, processing_df, quality_df = load_horsemeat_jerky_data()

# Основной интерфейс
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📊 Расчет питательности")
    
    # Выбор этапа продукта
    product_stage = st.selectbox(
        "Выберите этап продукта",
        options=nutrition_df['Этап'].values
    )
    
    # Ввод веса
    weight = st.number_input(
        "Вес (грамм)",
        min_value=1,
        max_value=500,
        value=50,
        step=10,
        help="Рекомендуемая порция: 20-50 г"
    )
    
    # Отображение параметров обработки
    st.subheader("🔧 Рекомендуемые параметры обработки")
    stage_index = nutrition_df[nutrition_df['Этап'] == product_stage].index[0]
    
    st.write(f"**Время засолки:** {processing_df['Время_засолки_дни'].iloc[stage_index]} дней")
    st.write(f"**Температура сушки:** {processing_df['Температура_сушки_℃'].iloc[stage_index]}℃")
    st.write(f"**Относительная влажность:** {processing_df['Относительная_влажность_%'].iloc[stage_index]}%")
    st.write(f"**Время сушки:** {processing_df['Время_сушки_дни'].iloc[stage_index]} дней")

with col2:
    st.header("📈 Анализ пищевой ценности")
    
    # Получение данных выбранного этапа
    stage_data = nutrition_df[nutrition_df['Этап'] == product_stage].iloc[0]
    
    # Расчет пищевой ценности
    weight_factor = weight / 100
    nutrition_results = {
        'Белки': stage_data['Белки_г'] * weight_factor,
        'Жиры': stage_data['Жиры_г'] * weight_factor,
        'Калории': stage_data['Калории_ккал'] * weight_factor,
        'Натрий': stage_data['Натрий_мг'] * weight_factor,
        'Железо': stage_data['Железо_мг'] * weight_factor,
        'Цинк': stage_data['Цинк_мг'] * weight_factor
    }
    
    # Отображение показателей питательности
    st.subheader(f"Пищевая ценность {weight}г {product_stage}")
    
    # Использование макета колонок для отображения показателей
    col2_1, col2_2, col2_3 = st.columns(3)
    
    with col2_1:
        st.metric("🔥 Калории", f"{nutrition_results['Калории']:.0f} ккал")
        st.metric("💪 Белки", f"{nutrition_results['Белки']:.1f} г")
        
    with col2_2:
        st.metric("🛢️ Жиры", f"{nutrition_results['Жиры']:.1f} г")
        st.metric("🧂 Натрий", f"{nutrition_results['Натрий']:.0f} мг")
        
    with col2_3:
        st.metric("🔴 Железо", f"{nutrition_results['Железо']:.1f} мг")
        st.metric("🔵 Цинк", f"{nutrition_results['Цинк']:.1f} мг")

# Визуальный анализ
st.header("📊 Анализ процесса вяления")

tab1, tab2, tab3 = st.tabs(["Изменение питательности", "Параметры обработки", "Контроль качества"])

with tab1:
    # Изменение пищевой ценности в процессе вяления
    fig1 = go.Figure()
    
    fig1.add_trace(go.Scatter(
        x=nutrition_df['Этап'], 
        y=nutrition_df['Белки_г'],
        mode='lines+markers',
        name='Белки',
        line=dict(color='blue', width=3)
    ))
    
    fig1.add_trace(go.Scatter(
        x=nutrition_df['Этап'], 
        y=nutrition_df['Влага_%'],
        mode='lines+markers',
        name='Влага',
        line=dict(color='green', width=3)
    ))
    
    fig1.update_layout(
        title="Изменение содержания белков и влаги в процессе вяления",
        xaxis_title="Этап обработки",
        yaxis_title="Содержание (г/100г)",
        height=400
    )
    
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    # Визуализация параметров обработки
    col1, col2 = st.columns(2)
    
    with col1:
        # Создание правильных данных для столбчатой диаграммы
        param_data = pd.DataFrame({
            'Параметр': ['Время засолки', 'Температура сушки', 'Относительная влажность'],
            'Значение': [
                processing_df['Время_засолки_дни'].mean(), 
                processing_df['Температура_сушки_℃'].mean(), 
                processing_df['Относительная_влажность_%'].mean()
            ]
        })
        
        fig2 = px.bar(
            param_data,
            x='Параметр',
            y='Значение',
            title="Средние параметры обработки",
            labels={'Значение': 'Значение'}
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    with col2:
        fig3 = px.line(
            processing_df,
            x=['Этап 1', 'Этап 2', 'Этап 3'],
            y='Время_сушки_дни',
            title="Требования ко времени сушки",
            markers=True
        )
        st.plotly_chart(fig3, use_container_width=True)

with tab3:
    # Графики контроля качества
    st.subheader("Показатели качества партий")
    
    fig4 = px.scatter(
        quality_df,
        x='Влага_%',
        y='Соль_%',
        color='Белки_%',
        size='pH',
        hover_data=['Партия'],
        title="Содержание влаги vs Содержание соли",
        labels={'Влага_%': 'Содержание влаги (%)', 'Соль_%': 'Содержание соли (%)'}
    )
    
    st.plotly_chart(fig4, use_container_width=True)
    
    # Статистика показателей качества
    st.subheader("Распределение показателей качества")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig5 = px.histogram(quality_df, x='Влага_%', title="Распределение содержания влаги")
        st.plotly_chart(fig5, use_container_width=True)
    
    with col2:
        fig6 = px.histogram(quality_df, x='Соль_%', title="Распределение содержания соли")
        st.plotly_chart(fig6, use_container_width=True)
    
    with col3:
        fig7 = px.histogram(quality_df, x='Белки_%', title="Распределение содержания белков")
        st.plotly_chart(fig7, use_container_width=True)

# Традиционные знания и рекомендации
st.header("💡 Традиционные знания о казахской вяленой конине")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🐎 Традиционная технология приготовления")
    st.info("""
    **Требования к сырью:**
    - Использование мышц крупа и спины взрослых лошадей
    - Мясо плотное, с равномерным распределением жира
    - Традиционно готовится осенью при подходящей температуре
    
    **Технологический процесс:**
    1. Соление (3-7 дней)
    2. Естественная сушка (15-30 дней)
    3. Регулярное переворачивание для равномерной сушки
    4. Контроль качества и упаковка
    """)

with col2:
    st.subheader("🏥 Рекомендации по употреблению и хранению")
    st.info("""
    **Рекомендации по употреблению:**
    - Рекомендуемая суточная порция: 20-50 г
    - Высокобелковая добавка, подходит спортсменам
    - Богата железом, профилактика анемии
    
    **Условия хранения:**
    - Хранить в сухом прохладном месте
    - Избегать прямого солнечного света
    - Срок годности: 6-12 месяцев
    - После вскрытия рекомендуется хранить в холодильнике
    """)

# Сохранение в файл
st.sidebar.header("💾 Экспорт данных")
if st.sidebar.button("Скачать данные о питательности"):
    csv = nutrition_df.to_csv(index=False)
    st.sidebar.download_button(
        label="Подтвердить скачивание CSV",
        data=csv,
        file_name=f"данные_питательности_вяленой_конины_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )

# Примечание в подвале
st.markdown("---")
st.markdown("""
**Примечание к данным:**
- На основе данных о традиционной казахской технологии вяления конины
- Пищевая ценность указана на 100 г съедобной части
- Параметры обработки являются рекомендуемыми значениями традиционной технологии
- Данные качества основаны на статистике реальных производственных партий
""")
