import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# =====================================================
# 1️⃣ 한글 폰트 설정 (중복 제거 · 단일 적용)
# =====================================================
font_path = os.path.join(os.getcwd(), "malgun.ttf")

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name
else:
    st.warning("⚠ malgun.ttf 폰트 파일을 찾을 수 없습니다.")

plt.rcParams["axes.unicode_minus"] = False

# =====================================================
# 2️⃣ Streamlit UI
# =====================================================
st.title("📊 국가산업단지 업종별 수출실적 분석")

file_path = "한국산업단지공단_국가산업단지 산업동향정보_업종별 수출실적_20250930.csv"

try:
    # -------------------------------------------------
    # 데이터 로드
    # -------------------------------------------------
    df = pd.read_csv(file_path, encoding="cp949")
    st.success("데이터 로드 완료!")

    st.subheader("데이터 확인")
    st.write(df.head())

    # -------------------------------------------------
    # 분석 컬럼 선택
    # -------------------------------------------------
    numeric_cols = df.columns.drop(["산업단지", "구분"]).tolist()

    selected_col = st.selectbox(
        "수출 실적을 비교할 업종을 선택하세요:",
        numeric_cols
    )

    # -------------------------------------------------
    # 그래프
    # -------------------------------------------------
    st.subheader(f"📍 산업단지별 {selected_col} 현황")

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

except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
