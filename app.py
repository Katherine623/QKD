import numpy as np
import plotly.graph_objects as go
import streamlit as st


def binary_entropy(x):
    """計算二元熵函數 h(x)。"""
    x = np.clip(x, 1e-10, 1 - 1e-10)
    return -x * np.log2(x) - (1 - x) * np.log2(1 - x)


def r_iso(e):
    """各向同性通道 (對應六態協定) 的金鑰率。"""
    e_adj = np.clip(1.5 * e, 1e-10, 1 - 1e-10)
    r = 1 - binary_entropy(e_adj) - e_adj * np.log2(3)
    return np.maximum(r, 0)


def r_ani(e):
    """各向異性通道 (Shor-Preskill 邊界) 的金鑰率。"""
    r = 1 - 2 * binary_entropy(e)
    return np.maximum(r, 0)


st.set_page_config(page_title="BB84 安全金鑰率分析", layout="wide")

st.markdown(
    """
<style>
    .stApp {
        background: linear-gradient(160deg, #edf2f7 0%, #f7fafc 100%);
    }
    .panel {
        background: #f8fafc;
        border: 1px solid #d7dee7;
        border-radius: 18px;
        padding: 18px 20px;
        margin-bottom: 14px;
    }
    .metric-card {
        background: #eef2f6;
        border: 1px solid #d2dbe5;
        border-radius: 14px;
        padding: 12px 14px;
        text-align: center;
    }
    .metric-title {
        color: #4a5568;
        font-size: 0.95rem;
        margin-bottom: 6px;
        font-weight: 600;
    }
    .metric-value {
        color: #1a202c;
        font-size: 1.25rem;
        font-weight: 700;
    }
    .value-box {
        background: #eef2f7;
        border: 1px solid #d7dee7;
        border-radius: 14px;
        padding: 14px;
        text-align: center;
    }
    .value-title {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.15rem;
        margin-bottom: 6px;
    }
    .value-number-blue {
        color: #1f5bc1;
        font-size: 3rem;
        line-height: 1;
        font-weight: 800;
    }
    .value-number-green {
        color: #0f7b2d;
        font-size: 3rem;
        line-height: 1;
        font-weight: 800;
    }
</style>
""",
    unsafe_allow_html=True,
)

if "qber" not in st.session_state:
    st.session_state["qber"] = 0.05

qber = float(st.session_state["qber"])

e_vals = np.linspace(0.0, 0.15, 600)
y_iso = r_iso(e_vals)
y_ani = r_ani(e_vals)

iso_now = float(r_iso(qber))
ani_now = float(r_ani(qber))

st.markdown("## 量子安全金鑰率分析 (BB84)")

head1, head2, head3 = st.columns(3)
with head1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">當前錯誤率</div>
            <div class="metric-value">{qber:.1%}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with head2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">SHOR-PRESKILL 速率</div>
            <div class="metric-value">{ani_now:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with head3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">六態協定速率</div>
            <div class="metric-value">{iso_now:.3f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=e_vals,
        y=y_ani,
        mode="lines",
        name="Shor-Preskill",
        line=dict(color="#1f5bc1", width=4),
        fill="tozeroy",
        fillcolor="rgba(31, 91, 193, 0.14)",
    )
)

fig.add_trace(
    go.Scatter(
        x=e_vals,
        y=y_iso,
        mode="lines",
        name="Six-state",
        line=dict(color="#0f7b2d", width=4),
    )
)

fig.add_trace(
    go.Scatter(
        x=[qber],
        y=[ani_now],
        mode="markers+text",
        text=["Shor-Preskill"],
        textposition="top center",
        marker=dict(size=12, color="#1f5bc1", line=dict(width=2, color="white")),
        name="當前點 (Shor-Preskill)",
        showlegend=False,
    )
)

fig.add_trace(
    go.Scatter(
        x=[qber],
        y=[iso_now],
        mode="markers+text",
        text=["Six-state"],
        textposition="top center",
        marker=dict(size=12, color="#0f7b2d", line=dict(width=2, color="white")),
        name="當前點 (Six-state)",
        showlegend=False,
    )
)

fig.add_vline(x=0.110, line_dash="dash", line_color="#4a5568", opacity=0.8)
fig.add_vline(x=0.126, line_dash="dash", line_color="#4a5568", opacity=0.8)

fig.add_annotation(
    x=0.110,
    y=0.04,
    text="Shor-Preskill 限制: 11.0%",
    showarrow=False,
    xanchor="right",
    font=dict(size=12, color="#2d3748"),
)
fig.add_annotation(
    x=0.126,
    y=0.08,
    text="六態協定限制: 12.6%",
    showarrow=False,
    xanchor="left",
    font=dict(size=12, color="#2d3748"),
)

fig.update_layout(
    height=520,
    paper_bgcolor="#f8fafc",
    plot_bgcolor="#f8fafc",
    margin=dict(l=35, r=30, t=20, b=40),
    xaxis=dict(
        title="錯誤率 (QBER)",
        tickformat=".0%",
        range=[0.0, 0.15],
        gridcolor="rgba(100, 116, 139, 0.20)",
    ),
    yaxis=dict(
        title="安全金鑰率 (Rate)",
        range=[0.0, 1.02],
        gridcolor="rgba(100, 116, 139, 0.20)",
    ),
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0.0),
)

st.plotly_chart(fig, use_container_width=True)

val1, val2 = st.columns(2)
with val1:
    st.markdown(
        f"""
        <div class="value-box">
            <div class="value-title">各向異性 (Shor-Preskill)</div>
            <div class="value-number-blue">{ani_now:.4f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with val2:
    st.markdown(
        f"""
        <div class="value-box">
            <div class="value-title">各向同性 (六態協定)</div>
            <div class="value-number-green">{iso_now:.4f}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

new_qber = st.slider(
    "量子位元錯誤率 (QBER)",
    min_value=0.0,
    max_value=0.15,
    value=float(qber),
    step=0.001,
    format="%.3f",
)

if new_qber != qber:
    st.session_state["qber"] = float(new_qber)
    st.rerun()

with st.expander("為什麼六態協定能容忍更高錯誤率？"):
    st.markdown(
        """
1. BB84 只監控兩個基底 (X/Z)，六態協定監控三個基底 (X/Y/Z)。
2. BB84 存在未完整監控方向，Eve 的攻擊自由度較高。
3. 六態協定限制 Eve 的不對稱攻擊，因此在相同 QBER 下可保留較高金鑰率。

對應結果是零金鑰率閾值不同：Shor-Preskill 約 11.0%，六態協定約 12.6%。
        """
    )