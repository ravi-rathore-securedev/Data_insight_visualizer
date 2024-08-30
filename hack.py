import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_sortables import sort_items

# Title of the app
st.title('Insight Data Visualization')

# Sidebar for chart selection, file upload, image upload, and statistics
with st.sidebar:
    st.header("Chart Selection")
    
    # File Upload
    uploaded_file = st.file_uploader("Upload Excel File", type="xlsx")
    
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
if uploaded_file is not None:
    # Read the Excel file into a DataFrame
    df = pd.read_excel(uploaded_file)
    
    # Display raw data
    st.subheader("Raw Data from Excel:")
    st.dataframe(df)

    # Define column names for X and Y axes
    x_column = 'UF 2-TotalPermeateFlow-ML/day'
    y_column = 'UF 2-PermeateTurbidity-NTU'

    # Generate KPI Table
    if kpi_selected:
        st.subheader("KPI Table")
        kpi_data = {
            'Total Rows': [len(df)],
            'Mean of X': [df[x_column].mean()],
            'Mean of Y': [df[y_column].mean()],
            'Max of X': [df[x_column].max()],
            'Max of Y': [df[y_column].max()],
            'Min of X': [df[x_column].min()],
            'Min of Y': [df[y_column].min()],
        }
        kpi_df = pd.DataFrame(kpi_data)
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
        fig_line = px.line(df, x=x_column, y=y_column, title=f'{y_column} vs {x_column}',
                           labels={x_column: x_column, y_column: y_column})
        chart_titles.append('Line Chart')
        chart_figures['Line Chart'] = fig_line
        
    if histogram_selected:
        fig_hist = px.histogram(df, x=y_column, nbins=10, title=f'Histogram of {y_column}',
                                labels={y_column: y_column})
        chart_titles.append('Histogram')
        chart_figures['Histogram'] = fig_hist
        
    if pie_chart_selected:
        df['Flow Categories'] = pd.cut(df[x_column], bins=5, labels=[f'Category {i}' for i in range(1, 6)])
        flow_category_counts = df['Flow Categories'].value_counts()
        fig_pie = px.pie(values=flow_category_counts, names=flow_category_counts.index, title='Flow Categories Distribution')
        chart_titles.append('Pie Chart')
        chart_figures['Pie Chart'] = fig_pie
        
    if scatter_plot_selected:
        fig_scatter = px.scatter(df, x=x_column, y=y_column, title=f'Scatter Plot of {y_column} vs {x_column}',
                                 labels={x_column: x_column, y_column: y_column})
        chart_titles.append('Scatter Plot')
        chart_figures['Scatter Plot'] = fig_scatter

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
