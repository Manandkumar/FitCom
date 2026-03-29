from supabase import create_client
import streamlit as st
import uuid

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def upload_image(file):
    try:
        file_ext = file.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"

        response = supabase.storage.from_("fitcom-images").upload(
            file_name,
            file.getvalue()
        )

        public_url = supabase.storage.from_("fitcom-images").get_public_url(file_name)

        return public_url

    except Exception as e:
        print("Upload error:", e)
        return None