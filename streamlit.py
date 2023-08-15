import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.sidebar.error('Error occurred while loading the file.'
                         ' Please make sure it is a valid CSV file.')
        return None


def explore_raw_data(df):
    st.subheader('Raw Data')
    if st.checkbox('Show Raw Data'):
        st.dataframe(df)


def data_cleaning(df):
    st.header('Data Cleaning')

    # Remove Missing Values
    st.subheader('Handling Missing Values')
    df.dropna(inplace=True)
    st.write("Missing values removed from the dataset.")

    # Remove Duplicate Rows
    st.subheader('Removing Duplicate Rows')
    initial_rows = len(df)
    df.drop_duplicates(inplace=True)
    final_rows = len(df)
    st.write(f"Removed {initial_rows - final_rows} duplicate rows.")

    if st.checkbox('Show Cleaned Data'):
        st.dataframe(df)


def data_analysis(df):
    st.header('Data Analysis')

    # Descriptive Statistics
    st.subheader('Descriptive Statistics')
    st.write(df.describe())

    # Correlation Matrix
    st.subheader('Correlation Matrix')
    corr_matrix = df.corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm',
                center=0, ax=ax)
    st.pyplot(fig)


def data_visualization(df):
    st.header('Data Visualization')

    # Histogram
    st.subheader('Histogram')
    selected_column = st.selectbox("Select a column to visualize:",
                                   df.columns)
    num_bins = st.slider("Select number of bins:",
                         min_value=5, max_value=50, value=20)
    plot_color = st.color_picker("Select histogram color", "#1f77b4")
    plt.figure(figsize=(8, 6))
    plt.hist(df[selected_column], bins=num_bins, edgecolor='black',
             color=plot_color, alpha=0.7)
    plt.xlabel(selected_column)
    plt.ylabel('Frequency')
    st.pyplot(plt)

    # Box Plot
    st.subheader('Box Plot')
    selected_column = st.selectbox("Select a column for box plot:",
                                   df.columns)
    plot_color = st.color_picker("Select box plot color", "#1f77b4")
    plt.figure(figsize=(8, 6))
    sns.boxplot(x=df[selected_column], color=plot_color)
    plt.xlabel(selected_column)
    plt.ylabel('Value')
    st.pyplot(plt)


def feedback_form():
    st.header('Feedback')
    with st.form('Feedback Form'):
        email = st.text_input("Your Email")
        feedback = st.text_area("Feedback")
        submitted = st.form_submit_button("Submit Feedback")
        if submitted:
            # Here, you can send the feedback to the developer's
            # email using external services/APIs
            st.success("Thank you for your feedback!")


def main():
    st.title('Data Cleaning, Analysis, and Visualization App')

    st.sidebar.header('Upload Dataset')
    uploaded_file = st.sidebar.file_uploader('Upload a CSV file', type=['csv'])

    agree_terms = st.sidebar.checkbox("I agree to the terms")

    if uploaded_file is not None and agree_terms:
        df = load_data(uploaded_file)

        if df is not None:
            explore_raw_data(df)
            data_cleaning(df)
            data_analysis(df)
            data_visualization(df)

            feedback_form()


if __name__ == '__main__':
    main()
