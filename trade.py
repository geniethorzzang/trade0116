import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform
import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os




# 폰트 파일 경로 지정 (파일이 파이썬 파일과 같은 폴더에 있어야 함)
font_path = os.path.join(os.getcwd(), 'malgun.ttf')

# 폰트가 있는지 확인 후 적용
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rc('font', family=font_prop.get_name())
else:
    st.warning("폰트 파일을 찾을 수 없어 기본 폰트를 사용합니다.")

plt.rcParams['axes.unicode_minus'] = False
# --- 한글 폰트 설정 ---
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("📊 국가산업단지 업종별 수출실적 분석")
file_path = "한국산업단지공단_국가산업단지 산업동향정보_업종별 수출실적_20250930.csv"

try:
    # 데이터 불러오기
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("데이터 로드 완료!")

    # 데이터 미리보기
    st.subheader("데이터 확인")
    st.write(df.head())

    # 분석 항목 선택 (수치 데이터가 있는 열만 필터링)
    # '산업단지'와 '구분'을 제외한 나머지 숫자 열들만 선택지로 제공
    numeric_cols = df.columns.drop(['산업단지', '구분']).tolist()
    selected_col = st.selectbox("수출 실적을 비교할 업종을 선택하세요:", numeric_cols)

    # 그래프 그리기
    st.subheader(f"📍 산업단지별 {selected_col} 현황")

    fig, ax = plt.subplots(figsize=(12, 6))
    
    # sns.barplot을 사용하여 x축에 산업단지명을 배치합니다.
    sns.barplot(data=df, x='산업단지', y=selected_col, ax=ax, palette='viridis')

    # 그래프 꾸미기
    plt.xticks(rotation=45)  # 단지 이름이 겹치지 않게 45도 회전
    ax.set_title(f"산업단지별 {selected_col} 수출액 비교", fontsize=15)
    ax.set_xlabel("산업단지명")
    ax.set_ylabel("수출액 (백만달러)")

    st.pyplot(fig)

except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")