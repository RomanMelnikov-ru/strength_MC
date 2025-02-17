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


# Функция для нахождения пересечения ребра с плоскостью
def find_intersection(edge_func, sigma_range, plane_constant, vertex, axis, c, phi, mode):
    sigma_values = sigma_range
    if axis == 1:  # sigma1 = sigma2 > sigma3 или sigma1 = sigma2 < sigma3
        sigma3 = edge_func(sigma_values, c, phi, mode)
        mask = sigma_values + sigma_values + sigma3 >= plane_constant
        if np.any(mask):
            idx = np.argmax(mask)
            return np.array([sigma_values[idx], sigma_values[idx], sigma3[idx]])
    elif axis == 2:  # sigma1 = sigma3 > sigma2 или sigma1 = sigma3 < sigma2
        sigma2 = edge_func(sigma_values, c, phi, mode)
        mask = sigma_values + sigma2 + sigma_values >= plane_constant
        if np.any(mask):
            idx = np.argmax(mask)
            return np.array([sigma_values[idx], sigma2[idx], sigma_values[idx]])
    elif axis == 3:  # sigma2 = sigma3 > sigma1 или sigma2 = sigma3 < sigma1
        sigma1 = edge_func(sigma_values, c, phi, mode)
        mask = sigma1 + sigma_values + sigma_values >= plane_constant
        if np.any(mask):
            idx = np.argmax(mask)
            return np.array([sigma1[idx], sigma_values[idx], sigma_values[idx]])
    return None


# Функция для обновления графика
def update(c, phi, plane_constant, camera_state=None):
    phi_rad = np.radians(phi)
    sigma_vertex = -c / np.tan(phi_rad)
    vertex = np.array([sigma_vertex, sigma_vertex, sigma_vertex])
    intersections = [
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 1, c, phi_rad, "12>3"),
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 2, c, phi_rad, "13>2"),
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 3, c, phi_rad, "23>1"),
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 1, c, phi_rad, "12<3"),
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 2, c, phi_rad, "13<2"),
        find_intersection(edge, np.linspace(sigma_vertex, 100, 1000), plane_constant, vertex, 3, c, phi_rad, "23<1")
    ]
    fig = go.Figure()

    # Рисуем ребра
    colors = ['red', 'red', 'red', 'red', 'red', 'red']
    for i, (intersection, color) in enumerate(zip(intersections, colors)):
        if intersection is not None:
            fig.add_trace(go.Scatter3d(
                x=[vertex[0], intersection[0]],
                y=[vertex[1], intersection[1]],
                z=[vertex[2], intersection[2]],
                mode='lines',
                line=dict(color=color, width=1),
                showlegend=False
            ))

    # Рисуем вершину
    fig.add_trace(go.Scatter3d(
        x=[vertex[0]],
        y=[vertex[1]],
        z=[vertex[2]],
        mode='markers',
        marker=dict(size=3, color='red'),
        showlegend=False
    ))

    # Рисуем оси
    fig.add_trace(go.Scatter3d(
        x=[0, 50], y=[0, 0], z=[0, 0],
        mode='lines',
        line=dict(color='green', width=2),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 50], z=[0, 0],
        mode='lines',
        line=dict(color='blue', width=2),
        showlegend=False
    ))
    fig.add_trace(go.Scatter3d(
        x=[0, 0], y=[0, 0], z=[0, 50],
        mode='lines',
        line=dict(color='red', width=2),
        showlegend=False
    ))

    # Рисуем гидростатическую ось
    hydrostatic_range = np.linspace(sigma_vertex, sigma_vertex + 100, 100)
    fig.add_trace(go.Scatter3d(
        x=hydrostatic_range,
        y=hydrostatic_range,
        z=hydrostatic_range,
        mode='lines',
        line=dict(color='grey', width=1, dash='dash'),
        showlegend=False
    ))

    # Рисуем грани пирамиды
    if all(intersection is not None for intersection in intersections):
        all_points = [vertex] + intersections
        x = [point[0] for point in all_points]
        y = [point[1] for point in all_points]
        z = [point[2] for point in all_points]
        # Индексы для граней
        i = [0, 0, 0, 0, 0, 0]  # Вершина пирамиды
        j = [5, 1, 6, 2, 4, 3]  # Первая точка грани
        k = [1, 6, 2, 4, 3, 5]  # Вторая точка грани
        fig.add_trace(go.Mesh3d(
            x=x, y=y, z=z,
            i=i, j=j, k=k,
            color='red',
            opacity=0.2,
            reversescale=True,
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

    # Сохраняем текущее состояние камеры
    if camera_state:
        fig.update_layout(scene_camera=camera_state)

    return fig


# Создаем слайдеры в Streamlit
c = st.slider('Удельное сцепление (кПа)', 0, 40, c_initial, key='c_slider')
phi = st.slider('Угол внутреннего трения (°)', 10, 30, phi_initial, key='phi_slider')
plane_constant = st.slider('Девиаторная плоскость (σ₁ + σ₂ + σ₃)', 0, 200, plane_constant_initial, key='plane_slider')

# Используем session state для сохранения состояния камеры
if 'camera_state' not in st.session_state:
    st.session_state['camera_state'] = dict(eye=dict(x=1.5, y=1.5, z=1.5))

# Обновляем и отображаем график
fig = update(c, phi, plane_constant, camera_state=st.session_state['camera_state'])
st.plotly_chart(fig)

# Сохраняем новое состояние камеры при взаимодействии с графиком
st.session_state['camera_state'] = fig.layout.scene.camera