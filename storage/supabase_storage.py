# ============================================================
# FitCom - Supabase Client (Auth + Storage)
# Author: Anand Kumar
# ============================================================

import streamlit as st
from supabase import create_client
import uuid


# ============================================================
# INIT SUPABASE CLIENT
# ============================================================

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("Supabase credentials missing in secrets.toml")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================================
# AUTH FUNCTIONS
# ============================================================

def sign_up(email: str, password: str):
    """
    Create a new user in Supabase Auth
    """
    try:
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })

        # Debug logging
        print("Signup response:", response)

        return response

    except Exception as e:
        print("Signup error:", e)
        return None


def sign_in(email: str, password: str):
    """
    Login existing user
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })

        # Debug logging
        print("Login response:", response)

        return response

    except Exception as e:
        print("Login error:", e)
        return None


def sign_out():
    """
    Logout current user
    """
    try:
        supabase.auth.sign_out()
    except Exception as e:
        print("Logout error:", e)


# ============================================================
# IMAGE UPLOAD
# ============================================================

def upload_image(file):
    """
    Upload image to Supabase Storage and return public URL
    """

    try:
        # Generate unique filename
        file_ext = file.name.split(".")[-1]
        file_name = f"{uuid.uuid4()}.{file_ext}"

        # Upload to bucket
        supabase.storage.from_("fitcom-images").upload(
            file_name,
            file.getvalue()
        )

        # Get public URL
        public_url = supabase.storage.from_("fitcom-images").get_public_url(file_name)

        return public_url

    except Exception as e:
        print("Image upload error:", e)
        return None