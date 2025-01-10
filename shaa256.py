import pandas as pd
import tkinter as tk
from tkinter import simpledialog, messagebox
import hashlib

# CSV faylini o'qish
file_path = '/home/shohruh/Downloads/world_population.csv'
df = pd.read_csv(file_path)

# SHA-256 hisoblash funksiyasi
def calculate_hash():
    original_data = entry_original.get()
    check_data = entry_check.get()

    if original_data:
        original_hash = hashlib.sha256(original_data.encode()).hexdigest()
        label_original_hash.config(text=f"Asl ma'lumotning SHA-256 xeshi: {original_hash}")

    if check_data:
        check_hash = hashlib.sha256(check_data.encode()).hexdigest()
        label_check_hash.config(text=f"Tekshirish ma'lumotining SHA-256 xeshi: {check_hash}")

        if original_hash == check_hash:
            messagebox.showinfo("Natija", "Ma'lumot o'zgarmagan. Xeshlar mos!")
        else:
            messagebox.showerror("Natija", "Ma'lumot buzilgan! Xeshlar mos emas!")

# CSV faylidan ma'lumot qidirish
def search_data():
    # Foydalanuvchidan nomni olish
    user_input = simpledialog.askstring("Input", "Iltimos, mamlakat nomini kiriting:")

    if user_input:
        # Kiritilgan nom asosida qidirish
        matching_rows = df[df['Country/Territory'].str.contains(user_input, case=False, na=False)]

        # Agar mos satrlar topilsa, ularni chiqarish
        if not matching_rows.empty:
            # Kerakli ustunlarni tanlash
            df_selected = matching_rows[['Country/Territory', 'Capital', '2022 Population', 'Area (km²)']]

            # Natijani formatlash
            df_selected['2022 Population'] = df_selected['2022 Population'].apply(lambda x: f"Odamlar soni: {x} ta")
            df_selected['Area (km²)'] = df_selected['Area (km²)'].apply(lambda x: f"Maydoni: {x} km²")

            # Har bir qatorni kerakli formatda o'zgartirish
            result_message = ""
            for _, row in df_selected.iterrows():
                result_message += f"Mamlakat: {row['Country/Territory']}, Poytaxti: {row['Capital']}, {row['2022 Population']}, {row['Area (km²)']}\n"

            # Natijani "Asl ma'lumotni kiriting" qatoriga joylashtirish
            entry_original.delete(0, tk.END)  # Kirish qatorini tozalash
            entry_original.insert(0, result_message)  # Natijani joylashtirish
        else:
            messagebox.showwarning("Xatolik", "Kiritilgan nom bo'yicha mos ma'lumotlar topilmadi!")

# Asosiy oynani yaratish
root = tk.Tk()
root.title("SHA-256 xeshlash va ma'lumot qidirish")

# 1-qator: Asl ma'lumotni kiritish
label_original = tk.Label(root, text="Siz yuborayotgan ma'lumot:")
label_original.pack()

entry_original = tk.Entry(root, width=50)
entry_original.pack()

# 2-qator: Tekshirish uchun ma'lumotni kiritish
label_check = tk.Label(root, text="Do'stingiz qabul qilayotgan ma'lumot:")
label_check.pack()

entry_check = tk.Entry(root, width=50)
entry_check.pack()

# Xeshlarni ko'rsatish
label_original_hash = tk.Label(root, text="Asl ma'lumotning SHA-256 xeshi:")
label_original_hash.pack()

label_check_hash = tk.Label(root, text="Tekshirish ma'lumotining SHA-256 xeshi:")
label_check_hash.pack()

# Xeshlarni taqqoslash tugmasi
button_compare = tk.Button(root, text="Xeshlarni taqqoslash", command=calculate_hash)
button_compare.pack()

# Ma'lumotni qidirish tugmasi
button_search = tk.Button(root, text="Mamlakatni qidirish", command=search_data)
button_search.pack()

# Oynani boshlash
root.mainloop()
