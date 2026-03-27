# python
import os
import streamlit as st
import plotly.express as px
import streamlit.components.v1 as components

st.set_page_config(page_title="Plotly XY click listener", layout="centered")
st.title("Click anywhere on the Plotly graph (listener method)")

# Create component files (index.html) once
COMP_DIR = os.path.join(os.path.dirname(__file__), "plotly_xy_click_component")
INDEX_HTML = os.path.join(COMP_DIR, "index.html")
os.makedirs(COMP_DIR, exist_ok=True)

HTML = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8" />
  <script src="https://cdn.plot.ly/plotly-2.26.0.min.js"></script>
  <script src="https://unpkg.com/streamlit-component-lib@1.2.0/dist/index.js"></script>
  <style>
    html, body { margin:0; padding:0; }
    #root { width: 100%; height: 100%; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script>
    const root = document.getElementById("root");
    let gd = null;
    let plotRect = null;
    let xRange = null, yRange = null;
    let xType = "linear", yType = "linear";

    function toMs(v) {
      if (v instanceof Date) return v.getTime();
      if (typeof v === "string") return Date.parse(v);
      return v;
    }

    function updateRanges() {
      if (!gd || !gd._fullLayout) return;
      const xl = gd._fullLayout.xaxis;
      const yl = gd._fullLayout.yaxis;
      xType = xl.type || "linear";
      yType = yl.type || "linear";
      const xr = xl.range || [xl._min, xl._max];
      const yr = yl.range || [yl._min, yl._max];
      xRange = (xType === "date") ? [toMs(xr[0]), toMs(xr[1])] : [xr[0], xr[1]];
      yRange = (yType === "date") ? [toMs(yr[0]), toMs(yr[1])] : [yr[0], yr[1]];

      const drag = gd.querySelector(".nsewdrag");
      plotRect = drag ? drag.getBoundingClientRect() : gd.getBoundingClientRect();
    }

    function computeXY(ev) {
      if (!plotRect || !xRange || !yRange) return null;
      const { clientX: cx, clientY: cy } = ev;
      if (cx < plotRect.left || cx > plotRect.right || cy < plotRect.top || cy > plotRect.bottom) return null;

      const nx = (cx - plotRect.left) / (plotRect.width || 1);
      const ny = (cy - plotRect.top) / (plotRect.height || 1);

      const x = xRange[0] + nx * (xRange[1] - xRange[0]);
      const y = yRange[0] + (1 - ny) * (yRange[1] - yRange[0]); // invert Y
      return { x, y };
    }

    function render(event) {
      const { fig, height } = event.detail.args;
      const h = height || 450;
      root.style.height = h + "px";

      if (!gd) {
        gd = document.createElement("div");
        gd.style.width = "100%";
        gd.style.height = "100%";
        root.appendChild(gd);
      }

      Plotly.react(gd, fig.data, fig.layout, { responsive: true }).then(() => {
        updateRanges();
        Streamlit.setFrameHeight(h);
      });

      gd.on("plotly_relayout", () => updateRanges());
      window.addEventListener("resize", () => updateRanges(), { passive: true });

      gd.addEventListener("mousedown", (ev) => {
        if (ev.button !== 0) return; // left-click only
        updateRanges();
        const xy = computeXY(ev);
        if (!xy) return;

        const payload = {
          x: (xType === "date") ? new Date(xy.x).toISOString() : xy.x,
          y: (yType === "date") ? new Date(xy.y).toISOString() : xy.y,
          ts: Date.now()
        };
        Streamlit.setComponentValue(payload);
      });
    }

    Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, render);
    Streamlit.setComponentReady();
  </script>
</body>
</html>
"""
if not os.path.exists(INDEX_HTML) or open(INDEX_HTML, "r", encoding="utf-8").read() != HTML:
    with open(INDEX_HTML, "w", encoding="utf-8") as f:
        f.write(HTML)

# Declare the component
plotly_xy_click = components.declare_component("plotly_xy_click", path=COMP_DIR)

def xy_click(fig, height=450, key=None):
    return plotly_xy_click(fig=fig.to_plotly_json(), height=height, key=key, default=None)

# Simple connected line figure
import pandas as pd
df = pd.DataFrame({"x": list(range(11)), "y": [0,1,1.5,2,3,2.5,4,3.5,5,4.5,6]})
fig = px.line(df, x="x", y="y", title="Click anywhere in the plot area")
fig.update_traces(mode="lines+markers")

# Use the listener component
click = xy_click(fig, height=420, key="listener")

st.subheader("Last click")
if click:
    st.json(click)
else:
    st.write("Click inside the plot area to see x/y here.")
