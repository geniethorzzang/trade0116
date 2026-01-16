import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import matplotlib.font_manager as fm
import os

# =====================================================
# [1] 한글 폰트 설정 (Cloud / 로컬 완전 대응)
# =====================================================
@st.cache_resource
def setup_korean_font():
    font_path = os.path.join(os.getcwd(), "NanumGothic.ttf")

    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        font_name = fm.FontProperties(fname=font_path).get_name()
        plt.rcParams["font.family"] = font_name
    else:
        st.warning("⚠️ NanumGothic.ttf 파일이 프로젝트에 없습니다.")

    plt.rcParams["axes.unicode_minus"] = False

setup_korean_font()

# =====================================================
# [2] Streamlit 메인 앱
# =====================================================
st.title("📊 데이터 통합 분석기")

# 데이터 파일 경로
file_path = "국세청_근로소득 백분위(천분위) 자료_20241231.csv"

if os.path.exists(file_path):
    try:
        # -------------------------------------------------
        # 데이터 로드
        # -------------------------------------------------
        df = pd.read_csv(file_path, encoding="cp949")
        st.success("✅ 데이터가 성공적으로 로드되었습니다!")

        # -------------------------------------------------
        # 데이터 미리보기
        # -------------------------------------------------
        st.subheader("🔍 데이터 미리보기")
        st.dataframe(df.head(10), use_container_width=True)

        # -------------------------------------------------
        # 데이터 요약
        # -------------------------------------------------
        with st.expander("📄 데이터 전체 요약 정보"):
            st.write(df.describe())

        # -------------------------------------------------
        # 시각화
        # -------------------------------------------------
        st.subheader("📈 통계 분포 그래프")

        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox(
                "분석할 항목을 선택하세요",
                numeric_cols
            )

            fig, ax = plt.subplots(figsize=(10, 5))

            sns.histplot(
                df[selected_col].dropna(),
                kde=True,
                color="#5A00E0",
                ax=ax
            )

            ax.set_title(
                f"[{selected_col}] 데이터 분포 확인",
                fontsize=15
            )
            ax.set_xlabel(selected_col)
            ax.set_ylabel("빈도수")

            st.pyplot(fig)

        else:
            st.warning("⚠️ 수치형 데이터가 없습니다.")

    except Exception as e:
        st.error(f"❌ 데이터 처리 중 오류 발생: {e}")

else:
    st.error(f"❌ 파일을 찾을 수 없습니다: {file_path}")

# =====================================================
# [3] 디버깅용 (Cloud에서 폰트 확인)
# =====================================================
with st.expander("🛠 폰트 설정 확인"):
    st.write("현재 matplotlib 폰트:", plt.rcParams["font.family"])
