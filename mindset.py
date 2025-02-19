import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="GEN AI", layout="wide")

st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 52px;
            font-weight: bold;
            background: linear-gradient(90deg, #FF416C, #FF4B2B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 3px 3px 6px rgba(0, 0, 0, 0.2);
            margin-bottom: 10px;
        }
        .description {
            text-align: center;
            font-size: 18px;
            color: #333;
            margin-top: 10px;
            margin-bottom: 50px;
        }
    </style>
    <h1 class="title">Smart Data Processor</h1>
    <p class="description">
        It is a powerful tool for uploading, cleaning, filtering, visualizing, and converting CSV and Excel files. 
    </p>
""", unsafe_allow_html=True)

upload_files = st.file_uploader("Upload your CSV and EXCEl files:", type=["csv", "xlsx"], accept_multiple_files=True)

if upload_files:
    for index, file in enumerate(upload_files):
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type {file_ext}")
            continue

        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024}")

        with st.expander(f"Preview {file.name}"):
            st.dataframe(df.head())

        with st.expander(f"Data Cleaning options for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove duplicates from {file.name}", key=f"remove_duplicates_{index}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates Removed!")

            with col2:
                if st.button(f"Fill Missing Value for {file.name}", key=f"fill_missing_{index}"):
                    numeric_col = df.select_dtypes(include=['number']).columns
                    df[numeric_col] = df[numeric_col].fillna(df[numeric_col].mean())
                    st.write("Missing Values have been Filled!")

        with st.expander(f"Data Filtering for {file.name}"):
            filter_col = st.selectbox(f"Select a column to filter by ({file.name}):", df.columns, key=f"filter_col_{index}")
            unique_values = df[filter_col].unique()
            filter_value = st.selectbox(f"Select value to filter {filter_col} ({file.name}):", unique_values, key=f"filter_value_{index}")
            df_filtered = df[df[filter_col] == filter_value]
            st.write("Filtered Data Preview:")
            st.dataframe(df_filtered)

        with st.expander(f"Select Columns to Convert for {file.name}"):
            columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns, key=f"columns_{index}")
            df = df[columns]

        with st.expander(f"Data Visualization for {file.name}"):
            if st.checkbox(f"Show Visualization for {file.name}", key=f"visualization_{index}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        with st.expander(f"Conversion Options for {file.name}"):
            conversion_type = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=f"conversion_type_{index}")
            if st.button(f"Convert {file.name}", key=f"convert_{index}"): 
                buffer = BytesIO() 
                if conversion_type == "CSV": 
                    df.to_csv(buffer, index=False) 
                    file_name = file.name.replace(file_ext, ".csv") 
                    mime_type = "text/csv" 
                elif conversion_type == "Excel": 
                    df.to_excel(buffer, index=False) 
                    file_name = file.name.replace(file_ext, ".xlsx") 
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" 
                buffer.seek(0)
                st.download_button(
                    label=f"Download {file_name} as {conversion_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type,
                )

st.success("All files processed!")