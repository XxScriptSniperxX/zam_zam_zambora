# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:02:59 2026

@tag: Xx_ScriptSniper_xX

@author: Albin
"""
import streamlit as st
import streamlit.components.v1 as components

# Declare the component
zoom_listener = components.declare_component(
    "zoom_listener",
    path="zoom_listener/frontend"   # folder containing index.html
)

# Use the component
ranges = zoom_listener()
st.write("Zoom state:", ranges)

if ranges:
    st.download_button(
        "⬇️ Download Zoom State",
        data=str(ranges),
        file_name="zoom_state.json",
        mime="application/json"
    )
