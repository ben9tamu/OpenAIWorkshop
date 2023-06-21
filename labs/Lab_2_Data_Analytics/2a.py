#Import neccessary libraries here
import numpy as np
import pandas as pd
import plotly.express as px
import sqlite3
import streamlit as st
from plotly.graph_objects import Figure

def show(data):
    if type(data) is Figure:
        st.plotly_chart(data)
    else:
        st.write(data)

conn = sqlite3.connect('data/northwind.db')  

#Query some data 
sql_query = '''
SELECT o.OrderDate, r.RegionDescription, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS Revenue
FROM Orders o
JOIN [Order Details] od ON o.OrderID = od.OrderID
JOIN Customers c ON o.CustomerID = c.CustomerID
JOIN EmployeeTerritories et ON o.EmployeeID = et.EmployeeID
JOIN Territories t ON et.TerritoryID = t.TerritoryID
JOIN Regions r ON t.RegionID = r.RegionID
WHERE o.OrderDate BETWEEN '2016-01-01' AND '2016-12-31'
GROUP BY o.OrderDate, r.RegionDescription
ORDER BY o.OrderDate
'''
step1_df = pd.read_sql_query(sql_query, conn) 

# Replace NAN with 0. Always have this step
step1_df['Revenue'] = step1_df['Revenue'].replace(np.nan,0)

#Calculate the total revenue in 2016
total_revenue = step1_df['Revenue'].sum()

#Calculate the top 20% customers based on their revenue contribution
top_20_percent_customers = step1_df.nlargest(int(len(step1_df)*0.2), 'Revenue')

#Calculate their percentage of revenue contribution
top_20_percent_revenue = top_20_percent_customers['Revenue'].sum()
top_20_percent_contribution = top_20_percent_revenue/total_revenue*100

#observe query result
print("step1_df", step1_df) #Always use observe() instead of print

step2_df = step1_df.groupby(['RegionDescription', 'OrderDate']).sum().reset_index()

#Visualize the data using plotly
fig = px.line(step2_df, x='OrderDate', y='Revenue', color='RegionDescription', title='Daily Revenue Trends in 2016 per Region')
show(fig)
