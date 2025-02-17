import plotly.graph_objects as go
import streamlit as st

# Функция для создания графика с осями
def create_axes():
    fig = go.Figure()

    # Рисуем оси
    fig.add_trace(go.Scatter3d(
        x=[0, 50], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='green', width=2),
        showlegend=False,
        name="σ₂"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 50], z=[0, 0],
        mode='lines',
        line=dict(color='blue', width=2),
        showlegend=False,
        name="σ₃"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, 50],
        mode='lines',
        line=dict(color='red', width=2),
        showlegend=False,
        name="σ₁"
    ))

    # Настройки графика
    fig.update_layout(
        title="3D Пространство с осями",
        scene=dict(
            xaxis_title="σ₂",
            yaxis_title="σ₃",
            zaxis_title="σ₁",
            aspectmode="cube",  # Сохраняем пропорции
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.5))  # Фиксированная камера
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    return fig

# Создаем и отображаем график в Streamlit
fig = create_axes()
st.plotly_chart(fig, key="axes_plot")
