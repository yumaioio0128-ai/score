import math
import streamlit as st

st.set_page_config(page_title="y→x 計算ツール", page_icon="🧮", layout="centered")
st.title("y → x 計算ツール")
st.caption("式:  x = 10^((y/0.0011392)^(1/6.497)) ／ y ≥ 0")

def calc_x(y: float) -> float:
    if y < 0:
        return float("nan")
    expo = (y / 0.0011392) ** (1/6.497) if y > 0 else 0.0
    return 10 ** expo

def sigfig_str(x: float, n: int) -> str:
    if x == 0 or math.isnan(x) or math.isinf(x):
        return str(x)
    return f"{x:.{n}g}"  # 有効数字n桁の文字列

def jp_unit_str(x: float, n: int) -> str:
    units = [
        (1e20, "垓"),
        (1e16, "京"),
        (1e12, "兆"),
        (1e8,  "億"),
        (1e4,  "万"),
    ]
    ax = abs(x)
    for scale, name in units:
        if ax >= scale:
            v = x / scale
            return f"{sigfig_str(v, n)}{name}"
    if ax < 1e4:
        return sigfig_str(x, n)
    return f"{x:.{n}e}"

with st.container(border=True):
    y = st.number_input("y を入力", min_value=0.0, value=13000.0, step=1.0)
    digits = st.slider("有効数字", 3, 8, 4)

    if y >= 0:
        x = calc_x(y)
        sci = f"{x:.{digits}e}"
        jp  = jp_unit_str(x, digits)
        st.metric("x（指数表記）", sci)
        st.write(f"日本語表記：**約 {jp}**")