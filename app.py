import streamlit as st
import pandas as pd
import io

# 웹 페이지 기본 설정
st.set_page_config(page_title="데이터 정제 자동화 툴", page_icon="📊", layout="wide")

# 타이틀 및 설명
st.title("📊 엑셀/CSV 데이터 자동 정제 툴")
st.write("파일을 업로드하면 데이터 요약을 확인하고, **중복 제거된 정제 파일**을 다운로드할 수 있습니다.")

st.divider()

# 1. 파일 업로드 섹션
uploaded_file = st.file_uploader("처리할 CSV 또는 엑셀(XLSX) 파일을 선택하세요", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # 파일 형식에 따른 데이터 읽기
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)

        st.success(f"✅ 파일 업로드 완료: **{uploaded_file.name}**")

        # 2. 데이터 요약 리포트 (컬럼 배치)
        col1, col2, col3 = st.columns(3)
        col1.metric("총 행(Row) 수", f"{len(df):,} 개")
        col2.metric("총 열(Column) 수", f"{len(df.columns)} 개")
        col3.metric("중복 행 수", f"{df.duplicated().sum():,} 개")

        # 데이터 미리보기
        st.subheader("🔍 데이터 미리보기 (상위 5개)")
        st.dataframe(df.head(), use_container_width=True)

        st.divider()

        # 3. 파일 정제 옵션
        st.subheader("🛠️ 데이터 정제 작업")
        remove_dup = st.checkbox("중복 데이터 제거하기", value=True)

        if remove_dup:
            df_cleaned = df.drop_duplicates()
            st.info(f"중복 제거 결과: {len(df):,}개 → **{len(df_cleaned):,}개** 데이터 남음")
        else:
            df_cleaned = df.copy()

        # 4. 정제된 파일 다운로드 버퍼 생성
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_cleaned.to_excel(writer, index=False, sheet_name='Cleaned_Data')
        processed_data = output.getvalue()

        # 다운로드 버튼
        st.download_button(
            label="📥 정제된 엑셀 파일 다운로드",
            data=processed_data,
            file_name=f"cleaned_{uploaded_file.name.split('.')[0]}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    except Exception as e:
        st.error(f"파일을 읽는 중 오류가 발생했습니다: {e}")

else:
    st.info("👆 위 영역에 파일을 드래그 앤 드롭하거나 클릭하여 선택해 주세요.")
