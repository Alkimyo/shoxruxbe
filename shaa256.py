import pandas as pd
import hashlib
import streamlit as st

# CSV faylini o'qish (GitHub yoki lokal fayl URL’idan o'qish mumkin)
file_path = 'world_population.csv'
df = pd.read_csv(file_path)

# SHA-256 hisoblash funksiyasi
def calculate_hash(original_data, check_data):
    if original_data:
        original_hash = hashlib.sha256(original_data.encode()).hexdigest()
        st.write(f"Asl ma'lumotning SHA-256 xeshi: {original_hash}")

    if check_data:
        check_hash = hashlib.sha256(check_data.encode()).hexdigest()
        st.write(f"Tekshirish ma'lumotining SHA-256 xeshi: {check_hash}")

        if original_hash == check_hash:
            st.success("Ma'lumot o'zgarmagan. Xeshlar mos!")
        else:
            st.error("Ma'lumot buzilgan! Xeshlar mos emas!")

# CSV faylidan ma'lumot qidirish
def search_data(user_input):
    if user_input:
        matching_rows = df[df['Country/Territory'].str.contains(user_input, case=False, na=False)]
        if not matching_rows.empty:
            df_selected = matching_rows[['Country/Territory', 'Capital', '2022 Population', 'Area (km²)']]
            df_selected['2022 Population'] = df_selected['2022 Population'].apply(lambda x: f"Odamlar soni: {x} ta")
            df_selected['Area (km²)'] = df_selected['Area (km²)'].apply(lambda x: f"Maydoni: {x} km²")

            result_message = ""
            for _, row in df_selected.iterrows():
                result_message += f"Mamlakat: {row['Country/Territory']}, Poytaxti: {row['Capital']}, {row['2022 Population']}, {row['Area (km²)']}\n"

            return result_message
        else:
            return "Kiritilgan nom bo'yicha mos ma'lumotlar topilmadi!"
    return ""

# Streamlit interfeysi
st.title("SHA-256 xeshlash va ma'lumot qidirish")

# Mamlakatni qidirish
user_input = st.text_input("Iltimos, mamlakat nomini kiriting:")
if user_input:
    result_message = search_data(user_input)
    st.text_area("Natija", result_message)

    # Mamlakatni topganidan so'ng xeshlarni taqqoslash
    original_data = st.text_input("Siz yuborayotgan ma'lumot:")
    check_data = st.text_input("Do'stingiz qabul qilayotgan ma'lumot:")

    if st.button("Xeshlarni taqqoslash"):
        calculate_hash(original_data, check_data)
