import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os
import numpy as np

# =====================================================
# 1️⃣ 한글 폰트 설정 (Cloud / 로컬 공통)
# =====================================================
@st.cache_resource
def setup_korean_font():
    font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")

    if not os.path.exists(font_path):
        st.error("❌ NanumGothic.ttf 파일이 프로젝트에 없습니다.")
        return

    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()

    plt.rcParams["font.family"] = font_name
    plt.rcParams["axes.unicode_minus"] = False

setup_korean_font()

# =====================================================
# 2️⃣ Streamlit UI
# =====================================================
st.title("📊 국가산업단지 업종별 수출실적 분석")

# =====================================================
# 3️⃣ 파일 업로드 (Cloud 필수 패턴)
# =====================================================
uploaded_file = st.file_uploader(
    "📂 CSV 파일 업로드 (cp949 인코딩)",
    type=["csv"]
)

if uploaded_file is None:
    st.warning("⬆ CSV 파일을 업로드해주세요.")
    st.stop()

# =====================================================
# 4️⃣ 데이터 로드
# =====================================================
try:
    df = pd.read_csv(uploaded_file, encoding="cp949")
    st.success("✅ 데이터 로드 완료!")
except Exception as e:
    st.error(f"데이터 로딩 실패: {e}")
    st.stop()

# =====================================================
# 5️⃣ 데이터 확인
# =====================================================
st.subheader("🔍 데이터 미리보기")
st.dataframe(df.head(), use_container_width=True)

# =====================================================
# 6️⃣ 분석 컬럼 선택
# =====================================================
exclude_cols = ["산업단지", "구분"]
numeric_cols = [c for c in df.columns if c not in exclude_cols]

if not numeric_cols:
    st.error("❌ 분석 가능한 수치형 컬럼이 없습니다.")
    st.stop()

selected_col = st.selectbox(
    "📌 수출 실적을 비교할 업종 선택",
    numeric_cols
)

# =====================================================
# 7️⃣ 시각화
# =====================================================
st.subheader(f"📍 산업단지별 {selected_col} 수출 실적")

fig, ax = plt.subplots(figsize=(12, 6))

sns.barplot(
    data=df,
    x="산업단지",
    y=selected_col,
    palette="viridis",
    ax=ax
)

ax.set_title(f"산업단지별 {selected_col} 수출액 비교", fontsize=15)
ax.set_xlabel("산업단지명")
ax.set_ylabel("수출액 (백만달러)")
plt.xticks(rotation=45)

st.pyplot(fig)

# =====================================================
# 8️⃣ 디버깅용 폰트 확인
# =====================================================
with st.expander("🛠 폰트 설정 확인"):
    st.write("현재 matplotlib 폰트:", plt.rcParams["font.family"])
