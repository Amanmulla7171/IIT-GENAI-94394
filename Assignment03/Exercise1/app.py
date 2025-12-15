import streamlit as st

st.title("File Uploader and Display")

# Add a lot of vertical space using markdown line breaks
st.markdown("---")
st.markdown("<br><br><br><br><br><br><br><br><br><br>", unsafe_allow_html=True)
st.markdown("---")

# The uploader will now appear much lower
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    file_details = {
        "Filename": uploaded_file.name,
        "FileType": uploaded_file.type,
        "FileSize": uploaded_file.size
    }
    st.write(file_details)
    st.text_area("File Content", uploaded_file.getvalue().decode("utf-8"), height=300)
else:
    st.write("No file uploaded yet.")


#apply sql query to uploaded file content if its a csv
if uploaded_file is not None and uploaded_file.type == "text/csv":
    import pandas as pd
    import sqlite3

    # Read the CSV file into a DataFrame
    df = pd.read_csv(uploaded_file)

    # Create an in-memory SQLite database
    conn = sqlite3.connect(':memory:')
    df.to_sql('table_name', conn, index=False, if_exists='replace')

    # Get the SQL query from the text area
    sql_query = st.text_area("SQL Query", "SELECT * FROM table_name;", height=100)

    if st.button("Run Query"):
        try:
            query_result = pd.read_sql_query(sql_query, conn)
            st.write(query_result)
        except Exception as e:
            st.error(f"An error occurred: {e}")