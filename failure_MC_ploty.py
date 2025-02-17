import numpy as np
import streamlit as st
import plotly.graph_objects as go

# Начальные параметры материала
c_initial = 10  # Начальное значение сцепления (кПа)
phi_initial = 30  # Начальное значение угла внутреннего трения (градусы)
plane_constant_initial = 100  # Начальное значение для плоскости

# Универсальная функция для вычисления sigma3 или sigma2 через sigma1 (или наоборот)
def edge(sigma, c, phi, mode):
    if mode == "12>3":
        return sigma - (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 + np.sin(phi))
    elif mode == "12<3":
        return sigma + (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 - np.sin(phi))
    elif mode == "13>2":
        return sigma - (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 + np.sin(phi))
    elif mode == "13<2":
        return sigma + (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 - np.sin(phi))
    elif mode == "23>1":
        return sigma - (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 + np.sin(phi))
    elif mode == "23<1":
        return sigma + (2 * c * np.cos(phi) + 2 * sigma * np.sin(phi)) / (1 - np.sin(phi))

# Функция для обновления графика
def update(c, phi, plane_constant):
    phi_rad = np.radians(phi)
    sigma_vertex = -c / np.tan(phi_rad)
    vertex = np.array([sigma_vertex, sigma_vertex, sigma_vertex])
    
    fig = go.Figure()
    
    # Рисуем оси
    fig.add_trace(go.Scatter3d(
        x=[0, 50], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='green', width=3, dash='dash'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 50], z=[0, 0],
        mode='lines',
        line=dict(color='blue', width=3, dash='dash'),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, 50],
        mode='lines',
        line=dict(color='red', width=3, dash='dash'),
        showlegend=False
    ))
    
    # Настройки графика
    fig.update_layout(
        title=f'Шестигранная пирамида прочности Мора-Кулона<br>c = {c:.1f} кПа, φ = {phi:.1f}°',
        scene=dict(
            xaxis_title='σ₂',
            yaxis_title='σ₃',
            zaxis_title='σ₁',
            aspectmode="cube"
        ),
        margin=dict(l=0, r=0, b=0, t=30)
    )
    
    return fig

# Создаем слайдеры в Streamlit
c = st.slider('Удельное сцепление (кПа)', 0, 40, c_initial, key='c_slider')
phi = st.slider('Угол внутреннего трения (°)', 10, 30, phi_initial, key='phi_slider')
plane_constant = st.slider('Девиаторная плоскость (σ₁ + σ₂ + σ₃)', 0, 200, plane_constant_initial, key='plane_slider')

# Обновляем и отображаем график
fig = update(c, phi, plane_constant)
st.plotly_chart(fig)
