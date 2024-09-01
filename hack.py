import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF
from io import BytesIO
import os
from streamlit_sortables import sort_items

# Title of the app
st.title('Insight Data Visualizer')

# Sidebar for chart selection, file upload, image upload, and statistics
with st.sidebar:
    st.header("Chart Selection")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")
    
    if uploaded_file is not None:
        # Read the Excel file into a DataFrame
        df = pd.read_excel(uploaded_file)
        
        # Assume the first column is the Timestamp or DateTime
        timestamp_column = df.columns[0]

        # Display column options for Y-axis selection (all columns except the timestamp)
        y_columns = st.multiselect("Select fields for Y-axis (you can select multiple):", df.columns[1:])
        
        # Checkboxes for selecting multiple chart types
        st.write("Select the charts you want to display:")
        line_chart_selected = st.checkbox("Line Chart")
        histogram_selected = st.checkbox("Histogram")
        pie_chart_selected = st.checkbox("Pie Chart")
        scatter_plot_selected = st.checkbox("Scatter Plot")

        # Image Upload
        st.header("Image Upload")
        uploaded_image = st.file_uploader("Upload an Image", type=["png", "jpg", "jpeg"])

        # Checkbox for displaying KPI Table and Statistics
        st.header("Additional Insights")
        kpi_selected = st.checkbox("Show KPI Table")
        statistics_selected = st.checkbox("Show Statistics")

# Main content area
if uploaded_file is not None and y_columns:
    # Display raw data
    st.subheader("Raw Data from Excel:")
    st.dataframe(df)

    # Generate KPI Table
    if kpi_selected:
        st.subheader("KPI Table")
        kpi_data = {
            'Total Rows': [len(df)],
            'Mean': df[y_columns].mean().tolist(),
            'Max': df[y_columns].max().tolist(),
            'Min': df[y_columns].min().tolist(),
        }
        kpi_df = pd.DataFrame(kpi_data, index=y_columns)
        st.table(kpi_df)

    # Display Statistics
    if statistics_selected:
        st.subheader("Statistics Overview")
        st.write(df.describe())

    # Prepare a list to hold chart titles and a dictionary for storing figures
    chart_titles = []
    chart_figures = {}

    # Generate the selected charts
    if line_chart_selected:
        fig_line = px.line(df, x=timestamp_column, y=y_columns, title=f'Line Chart: {", ".join(y_columns)} vs {timestamp_column}')
        chart_titles.append('Line Chart')
        chart_figures['Line Chart'] = fig_line
        
    if histogram_selected:
        for y_column in y_columns:
            fig_hist = px.histogram(df, x=y_column, nbins=10, title=f'Histogram of {y_column}')
            chart_titles.append(f'Histogram of {y_column}')
            chart_figures[f'Histogram of {y_column}'] = fig_hist
        
    if pie_chart_selected:
        for y_column in y_columns:
            bins = pd.cut(df[y_column], bins=5)
            bin_counts = bins.value_counts()
            bin_labels = [str(interval) for interval in bin_counts.index]
            
            fig_pie = px.pie(values=bin_counts, names=bin_labels, title=f'Pie Chart of {y_column} Distribution')
            chart_titles.append(f'Pie Chart of {y_column}')
            chart_figures[f'Pie Chart of {y_column}'] = fig_pie
        
    if scatter_plot_selected:
        for y_column in y_columns:
            fig_scatter = px.scatter(df, x=timestamp_column, y=y_column, title=f'Scatter Plot of {y_column} vs {timestamp_column}')
            chart_titles.append(f'Scatter Plot of {y_column}')
            chart_figures[f'Scatter Plot of {y_column}'] = fig_scatter

    # Render the charts in an interchangeable way
    sorted_titles = sort_items(chart_titles)

    # Display the charts in the order selected by the user
    for title in sorted_titles:
        st.subheader(title)
        st.plotly_chart(chart_figures[title], use_container_width=True)

    # Display the uploaded image if available
    if uploaded_image is not None:
        st.subheader("Uploaded Image:")
        st.image(uploaded_image, use_column_width=True)

    # Add a button to download the report as PDF
    if st.button("Download Report as PDF"):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, 'Insight Data Visualizer Report', ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, "Raw Data and Insights")

        # Create a list of sorted figures for PDF export
        for title in sorted_titles:
            img_path = f"{title}.png"
            if title in chart_figures:
                chart_figures[title].write_image(img_path)
                pdf.add_page()
                pdf.cell(0, 10, title, ln=True, align='C')
                pdf.image(img_path, x=10, y=20, w=180)
                os.remove(img_path)

        pdf_output = BytesIO()
        pdf.output(pdf_output)
        pdf_output.seek(0)

        st.download_button(label="Download PDF", data=pdf_output, file_name="Insight_Data_Visualizer_Report.pdf", mime="application/pdf")
else:
    st.write("Please upload an Excel file and select at least one Y-axis field to proceed.")
