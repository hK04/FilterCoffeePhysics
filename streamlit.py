import streamlit as st
from streamlit_option_menu import option_menu

import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from brewing_analysis import coffee_analysis
from plot import plot_brewing_chart, plotly_brewing_chart, plotly_extraction_charts

with st.sidebar:
    selected   = option_menu(
        menu_title = "Menu",
        options    = ["Экстракция", "О нас"],
        icons      = ["house", "envelope"],
        menu_icon  = "cast",
        default_index = 0,
        #orientation = "horizontal",
    )

    language   = st.selectbox(
        "Language/Язык",
        ("English", "Russian"),
    )

if selected == "Экстракция":
    analyser = coffee_analysis(x=np.load('data/refractometry.nbpy'))

    st.markdown('# Руководство по заварке кофе')

    st.markdown('#### Для расчета возможных вариантов экстракции необходимо загрузить калибровочные* данные')

    inn_col1, inn_col2, inn_col3 = st.columns(3)
    with inn_col1:
        coffee_mass = st.number_input("Масса кофе, г", value=8.79)
    with inn_col2:
        volume_it   = st.number_input("Объем пролива, мл", value=25)
    with inn_col3:
        temperature = st.number_input(r"Температура, $^\circ C$", value=95)
    
    st.markdown('По заданным физическим параметрам калибровки, получаем TDS% и EY% и оценку вкуса')

    st.markdown('### 1. Калибровочный график TDS, % от N')
    st.markdown('(Калибровочный график, показывает какой TDS у сэмпла кофе за i-ый пролив)')

    fig1 = px.scatter(
        pd.DataFrame({
                    'N, iteration': np.arange(1, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : analyser.tds_from_refr()
                    }),
        x='N, iteration',
        y='TDS, %'
    )

    fig1.add_trace(px.line(pd.DataFrame({
                    'N, iteration': np.arange(1, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : analyser.tds_from_refr()
                    }),
        x='N, iteration',
        y='TDS, %',).data[0])
                                    

    event = st.plotly_chart(fig1, on_select="rerun")
    
    st.markdown('### 2. Суммарные концентрация TDS, % и Выход EY, % в стакане от N пролива')

    fig2 = make_subplots(rows=1, cols=2)

    fig2.add_trace(
        px.scatter(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'EY, %' : np.concatenate([[0], analyser.mass_from_tds(bevarage=volume_it) / coffee_mass * 100]),
                    }),
                   x = 'N, iteration',
                   y = 'EY, %').data[0],
        row=1,
        col=1,
    )
    
    fig2.add_trace(
        px.line(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'EY, %' :  np.concatenate([[0], analyser.mass_from_tds(bevarage=volume_it) / coffee_mass * 100]),
                    }),
                   x = 'N, iteration',
                   y = 'EY, %').data[0],
        row=1,
        col=1
    )

    fig2.add_hline(y=18, line_dash="dash", row=1, col=1, line_color='red')
    fig2.add_hline(y=22, line_dash="dash", row=1, col=1, line_color='red')

    fig2.add_trace(
        px.scatter(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : np.concatenate([[0], analyser.tds_integral()])
                    }),
                   x = 'N, iteration',
                   y = 'TDS, %').data[0],
        row=1,
        col=2,
    )

    fig2.add_trace(
        px.line(pd.DataFrame({
                    'N, iteration' : np.arange(0, len(analyser.tds_from_refr()) + 1), 
                    'TDS, %' : np.concatenate([[0], analyser.tds_integral()])
                    }),
                   x = 'N, iteration',
                   y = 'TDS, %').data[0],
        row=1,
        col=2
    )

    fig2.add_hline(y=1.20, line_dash="dash", row=1, col=2, line_color='red')
    fig2.add_hline(y=1.45, line_dash="dash", row=1, col=2, line_color='red')

    fig2.update_xaxes(title_text="N, iteration", row=1, col=1)
    fig2.update_xaxes(title_text="N, iteration", row=1, col=2)

    fig2.update_yaxes(title_text="EY, %", row=1, col=1)
    fig2.update_yaxes(title_text="TDS, %", row=1, col=2)


    event2 = st.plotly_chart(fig2, on_select="rerun")

    st.markdown('### 3. Вкус кофе')
    st.markdown('(По умолчанию, все проливы сложены, т.к образуют единый напиток)')

    n_flows = st.slider("Колличество проливов для использования", min_value=1, max_value=len(analyser.tds_from_refr()), value=len(analyser.tds_from_refr()))
    flows = np.arange(n_flows)

    for row in range(n_flows // 4 + 1):
        columns = st.columns(4)
        for i, column in enumerate(columns):
            with column:
                if 4 * row + i < n_flows :
                    flows[4*row + i] = st.number_input(f"Пролив №{4 * row + i + 1}", min_value=0, max_value=10, step=1, value=1)

    coffe_auto_button = st.button('Авто')#, on_click=analyser.auto(bevarage=volume_it, coffee_mass=coffee_mass))

    #brewing_fig, brewing_ax = plot_brewing_chart() 
    x_point, y_point = analyser.estimate(flows, bevarage=volume_it, coffee_mass=coffee_mass)
    #brewing_ax.scatter(x_point, y_point, label='Coffee cup', color='red')
    #brewing_ax.legend(fontsize=20)

    #st.pyplot(brewing_fig)

    #st.markdown(flows)


    fig3 = px.scatter(pd.DataFrame({
                    'EY, %'  : [x_point], 
                    'TDS, %' : [y_point]
                    }),
                   x = 'EY, %',
                   y = 'TDS, %',
                   size=[0.1],
                   width=1600, height=800)
    fig3 = plotly_brewing_chart(fig3)

    st.plotly_chart(fig3)

    st.markdown(f"##### Выбранное кофе объемом `{flows.sum() * volume_it} мл` требует `{flows.max()}` дрип-пакетов")