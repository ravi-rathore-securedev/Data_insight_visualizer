import streamlit as st
import pandas as pd
import plotly.express as px

# Title of the app
st.title('Interactive Excel Data Visualization')

# File Upload
uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.write("Raw Data from Excel:")
    st.dataframe(df)

    # Define column names for X and Y axes
    x_column = 'UF 2-TotalPermeateFlow-ML/day'
    y_column = 'UF 2-PermeateTurbidity-NTU'

    # Dropdown menu for selecting chart type
    chart_type = st.selectbox(
        "Select the type of chart you want to display",
        ("Line Chart", "Histogram", "Pie Chart", "Scatter Plot")
    )

    # Check if the necessary columns exist in the data
    if x_column in df.columns and y_column in df.columns:
        # Generate the selected chart
        if chart_type == "Line Chart":
            fig = px.line(df, x=x_column, y=y_column, title=f'{y_column} vs {x_column}',
                          labels={x_column: x_column, y_column: y_column})
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Histogram":
            fig = px.histogram(df, x=y_column, nbins=10, title=f'Histogram of {y_column}',
                               labels={y_column: y_column})
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Pie Chart":
            df['Flow Categories'] = pd.cut(df[x_column], bins=5, labels=[f'Category {i}' for i in range(1, 6)])
            flow_category_counts = df['Flow Categories'].value_counts()
            fig = px.pie(values=flow_category_counts, names=flow_category_counts.index, title='Flow Categories Distribution')
            st.plotly_chart(fig, use_container_width=True)
        
        elif chart_type == "Scatter Plot":
            fig = px.scatter(df, x=x_column, y=y_column, title=f'Scatter Plot of {y_column} vs {x_column}',
                             labels={x_column: x_column, y_column: y_column})
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.write(f"Columns '{x_column}' and '{y_column}' not found in the data. Please upload an Excel file with these columns.")
