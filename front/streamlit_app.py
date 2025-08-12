import streamlit as st
import requests
import base64

st.title("Детекция ветрогенераторов")

tab1, tab2 = st.tabs(['По ссылке', 'Загрузка файла'])

FASTAPI_URL = "http://130.193.57.243:8000/"

def show_results(res):
    if "image_with_boxes" in res:
        st.subheader("Результат детекции")
        img_bytes = base64.b64decode(res["image_with_boxes"])
        st.image(img_bytes, caption="Детектированные объекты", use_container_width=True)
        st.write("Обнаруженные объекты:")
        for det in res["detections"]:
            st.json(det)
    else:
        st.error("Нет результата детекции")

with tab1:
    st.header("Детекция по URL")
    url = st.text_input("Введите ссылку на изображение")
    if st.button("Отправить по URL") and url:
        data = {"url": url}
        try:
            response = requests.post(f"{FASTAPI_URL}/det_image_url", json=data)
            res = response.json()
            show_results(res)
        except Exception as e:
            st.error(f"Ошибка: {e}")

with tab2:
    st.header("Детекция по загруженному файлу")
    uploaded_file = st.file_uploader("Загрузите изображение", type=["jpg", "jpeg", "png"])
    if st.button("Отправить файл") and uploaded_file is not None:
        files = {"file": uploaded_file.getvalue()}
        try:
            response = requests.post(f"{FASTAPI_URL}/det_image_file", files=files)
            res = response.json()
            show_results(res)
        except Exception as e:
            st.error(f"Ошибка: {e}")