import streamlit as st
import math
import matplotlib.pyplot as plt
import numpy as np

def calculate_parameters(material, fc, ft):
    if fc <= 0 or ft <= 0:
        st.error("Прочность на сжатие и растяжение должны быть положительными числами.")
        return
    
    # Определение диапазонов для материала
    if material == "Кирпичная кладка":
        c_range = "0.1–1 МПа"
        phi_range = "20–30 градусов"
    elif material == "Бетон":
        c_range = "1–10 МПа"
        phi_range = "30–40 градусов"
    else:
        st.error("Неизвестный материал.")
        return
    
    # Расчет параметров
    c = (fc * ft) / (fc + ft)
    phi_rad = math.atan((fc - ft) / (fc + ft))
    phi_deg = math.degrees(phi_rad)
    
    # Вывод результатов
    result_text = (
        f"Материал: {material}\n"
        f"Сцепление (c): {c:.2f} МПа (рекомендуемый диапазон: {c_range})\n"
        f"Угол внутреннего трения (φ): {phi_deg:.2f} градусов (рекомендуемый диапазон: {phi_range})\n\n"
        f"Рекомендации:\n"
        f"- Учитывайте, что параметры прочности могут изменяться в зависимости от условий эксплуатации (влажность, температура, длительные нагрузки).\n"
        f"- Для точных расчетов (например, для ответственных конструкций) рекомендуется проводить экспериментальные испытания."
    )
    st.success(result_text)
    
    # Построение графика закона Кулона
    plot_coulomb_law(c, phi_rad)

def plot_coulomb_law(c, phi_rad):
    # Диапазон нормальных напряжений (σ)
    sigma = np.linspace(0, 10, 100)  # от 0 до 10 МПа
    # Касательное напряжение (τ) по закону Кулона
    tau = c + sigma * math.tan(phi_rad)
    
    # Построение графика
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(sigma, tau, label=r"$\tau = c + \sigma \cdot \tan(\phi)$", color="blue")
    ax.set_title("Закон Кулона")
    ax.set_xlabel(r"Нормальное напряжение $\sigma$, МПа")
    ax.set_ylabel(r"Касательное напряжение $\tau$, МПа")
    ax.grid(True)
    ax.legend()
    
    # Отображение графика в Streamlit
    st.pyplot(fig)

# Создание пользовательского интерфейса в Streamlit
st.title("Расчет параметров Мора-Кулона")

# Выбор материала
material = st.selectbox("Выберите материал:", ["Кирпичная кладка", "Бетон"])

# Ввод прочности на сжатие (fc)
fc = st.number_input("Прочность на сжатие (fc), МПа:", min_value=0.01, value=10.0, step=0.1)

# Ввод прочности на растяжение (ft)
ft = st.number_input("Прочность на растяжение (ft), МПа:", min_value=0.01, value=1.0, step=0.1)

# Кнопка для расчета
if st.button("Рассчитать"):
    calculate_parameters(material, fc, ft)

# Цитирование
st.write("Расчет основан на работах:")
st.write("- Chen, W. F. (1982). Plasticity in Reinforced Concrete")
st.write("- Neville, A. M. (2011). Properties of Concrete")
