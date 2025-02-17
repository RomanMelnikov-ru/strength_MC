import streamlit as st
import math

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
    
    # Используйте st.empty() для управления выводом текста
    text_placeholder = st.empty()
    with text_placeholder:
        st.success(result_text)

# Создание пользовательского интерфейса в Streamlit
st.title("Расчет параметров Мора-Кулона")

# Выбор материала
material = st.selectbox("Выберите материал:", ["Кирпичная кладка", "Бетон"], key="material_select")

# Ввод прочности на сжатие (fc)
fc = st.number_input("Прочность на сжатие (fc), МПа:", min_value=0.01, value=10.0, step=0.1, key="fc_input")

# Ввод прочности на растяжение (ft)
ft = st.number_input("Прочность на растяжение (ft), МПа:", min_value=0.01, value=1.0, step=0.1, key="ft_input")

# Кнопка для расчета
if st.button("Рассчитать", key="calculate_button"):
    calculate_parameters(material, fc, ft)

# Цитирование
st.write("Расчет основан на работах:")
st.write("- Chen, W. F. (1982). Plasticity in Reinforced Concrete")
st.write("- Neville, A. M. (2011). Properties of Concrete")
