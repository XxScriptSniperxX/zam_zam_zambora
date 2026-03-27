# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 14:02:59 2026

@tag: Xx_ScriptSniper_xX

@author: Albin
"""
import streamlit as st
import plotly.express as px
from streamlit_plotly_events2 import plotly_events
import pandas as pd

st.set_page_config(page_title="plotly_events minimal test", layout="centered")
st.title("Minimal plotly_events test (line plot)")

# Simple data
df = pd.DataFrame({
    "x": list(range(1, 11)),
    "y": [2, 1, 3, 5, 4, 6, 7, 5, 8, 9]
})

# Line chart with markers (points are clickable/selectable)
fig = px.line(df, x="x", y="y", title="Click points on the line")
fig.update_traces(mode="lines", marker=dict(size=8))

# Listen for click events
events = plotly_events(
    fig,
    click_event=True,
    hover_event=True,
    select_event=False,
    key="simple_line"
)

st.write("Events:", events)
if events:
    ev = events[0]
    st.success(f"Clicked point -> x={ev.get('x')}, y={ev.get('y')}, "
               f"curve={ev.get('curveNumber')}, point={ev.get('pointNumber')}")

