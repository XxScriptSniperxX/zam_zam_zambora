# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:02:59 2026

@tag: Xx_ScriptSniper_xX

@author: Albin
"""
import streamlit as st
import streamlit.components.v1 as components

zoom_listener = components.declare_component(
    "zoom_listener",
    path=r"C:\project files\General_PostP_tool\scratch"
)

ranges = zoom_listener()
st.write("Zoom state:", ranges)
