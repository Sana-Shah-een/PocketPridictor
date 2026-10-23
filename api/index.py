"""Vercel ASGI entrypoint for the PocketPredict Streamlit app."""

from pathlib import Path

import streamlit as st


app = st.App(Path(__file__).resolve().parents[1] / "app.py")
