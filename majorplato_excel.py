import streamlit as st
import json
import csv
import os
from datetime import datetime

st.set_page_config(page_title="Major Plato CSV Saver", layout="centered")

st.title("📋 Major Plato Decision Export")
st.markdown("Paste your JSON export from ChatGPT below:")

input_json = st.text_area("Game decision data (JSON format)", height=300)

if st.button("💾 Save CSV"):
    try:
        data = json.loads(input_json)
        player = data["player"].replace(" ", "_")
        unit = data["unit"].replace(" ", "_")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{player}_{unit}_{timestamp}.csv"
        save_path = os.path.join("saves", filename)
        os.makedirs("saves", exist_ok=True)

        with open(save_path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(["Időpont", "Döntés", "Etikai", "Katonai", "Parancsnoki"])
            for row in data["decisions"]:
                writer.writerow(row)

        st.success(f"✅ CSV fájl mentve: `{filename}`")
        with open(save_path, "rb") as f:
            st.download_button("⬇️ CSV letöltése", f, file_name=filename, mime="text/csv")

    except Exception as e:
        st.error(f"❌ Hiba: {str(e)}")
