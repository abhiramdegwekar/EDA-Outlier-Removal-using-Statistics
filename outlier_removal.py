import contextlib
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def outlier_removal(data,target_col):
    
    Q1 = np.percentile(data[target_col], 25, interpolation = 'midpoint')
    Q3 = np.percentile(data[target_col], 75, interpolation = 'midpoint')

    IQR = Q3 -Q1
    lower_limit = Q1 - 1.5*IQR
    upper_limit = Q3 + 1.5*IQR

    data_out = data[(data[target_col] > lower_limit) & (data[target_col] < upper_limit)]

    outlier_percent = ((len(data.index) - len(data_out.index))/len(data.index))*100
    st.write("Outlier present(in %) in your data is:", outlier_percent)

    raw_drop = len(data.index) - len(data_out.index)
    st.write("Number of rows will be dropped:", raw_drop)
    user_choice = st.selectbox("Do you want to remove/drop it ? If Yes enter 'Yes' else enter 'No' for No:", options=['Yes', 'No'])

    st.write("Your choice is:", user_choice)

    if user_choice == 'Yes':
        return download(data,data_out,target_col)
    st.write("Returning original data")
    st.write(data.head())
    return data


def download(uploaded_df,data_out,target_col):
    st.write("Outlier from your data has been removed")
    fig4 = plt.figure()
    sns.boxplot(data_out[target_col])
    st.write(fig4)
    st.write(data_out.head())
    st.download_button(label="Download the new data as CSV", data=uploaded_df.to_csv().encode('utf-8'), file_name='outlier_removed.csv', mime='text/csv')
    return data_out


def app():
    st.header('Outlier Removal from Data')
    st.markdown('#### Load your data here')
    uploaded_df = st.file_uploader("", type=["csv"])
    if uploaded_df is not None:
        uploaded_df = pd.read_csv(uploaded_df)
        st.write(uploaded_df.head())
        x_var = st.selectbox('In case you want see scatter plot Select the column for x axis', options=uploaded_df.columns)
        y_var = st.selectbox('In case you want see scatter plot Select the column for y axis', options=uploaded_df.columns
        )
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(1,1,1)
        plt.scatter(uploaded_df[x_var], uploaded_df[y_var])
        plt.xlabel(x_var)
        plt.xticks(rotation=90)
        plt.ylabel(y_var)
        st.pyplot(fig2)
        st.markdown('Select the column to check for outliers, i.e normally your target column')
        target_col = st.selectbox("Select the column in which you want to remove outlier", uploaded_df.columns)
        st.write(uploaded_df[target_col].head())
        with contextlib.suppress(Exception):
            fig3 = plt.figure()
            ax3 = fig3.add_subplot(1, 1, 1)            
            sns.boxplot(uploaded_df[target_col])
            st.pyplot(fig3)
            outlier_removal(uploaded_df,target_col)
            
            
app()       
