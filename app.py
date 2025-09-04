import pandas as pd
import streamlit as st
from io import BytesIO

st.title("Department Name Replacer")

st.write("Upload your Excel file and this tool will replace short department codes with full names in **Sheet1_Students**.")

# File uploader
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Mapping dictionary
replace_dict = {
    "CSE": "Department of Computer Science and Engineering",
    "SOM": "School of Management",
    "SOL": "School of Law",
    "SOB": "School of Business",
    "MDE": "Department of Multidisciplinary Engneering"
}

if uploaded_file is not None:
    # Read Excel
    xls = pd.ExcelFile(uploaded_file)

    # Process Sheet1_Students
    df_students = pd.read_excel(uploaded_file, sheet_name="Sheet1_Students")
    df_students["department"] = df_students["department"].str.upper().replace(replace_dict)

    # Load Sheet2_Teachers (unchanged)
    df_teachers = pd.read_excel(uploaded_file, sheet_name="Sheet2_Teachers")

    # Save to a new Excel file in memory
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df_students.to_excel(writer, sheet_name="Sheet1_Students", index=False)
        df_teachers.to_excel(writer, sheet_name="Sheet2_Teachers", index=False)
    output.seek(0)

    # Download button
    st.download_button(
        label="Download Updated Excel",
        data=output,
        file_name="filtered_attendance_updated.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    st.success("File processed successfully!")
