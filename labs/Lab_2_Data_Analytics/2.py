#Import neccessary libraries here
import numpy as np
import pandas as pd
import plotly.express as px
import sqlite3

conn = sqlite3.connect('data/northwind.db')  

#Query some data 
sql_query = '''
SELECT o.CustomerID, SUM(od.UnitPrice * od.Quantity * (1 - od.Discount)) AS Revenue
FROM Orders o
JOIN [Order Details] od ON o.OrderID = od.OrderID
WHERE strftime('%Y', o.OrderDate) = '2016'
GROUP BY o.CustomerID
ORDER BY Revenue DESC
'''
customer_revenue_df = pd.read_sql_query(sql_query, conn) 

# Replace NAN with 0. Always have this step
customer_revenue_df['Revenue'] = customer_revenue_df['Revenue'].replace(np.nan,0)

#Calculate the total revenue in 2016
total_revenue = customer_revenue_df['Revenue'].sum()

#Calculate the top 20% customers based on their revenue contribution
top_20_percent_customers = customer_revenue_df.nlargest(int(len(customer_revenue_df)*0.2), 'Revenue')

#Calculate their percentage of revenue contribution
top_20_percent_revenue = top_20_percent_customers['Revenue'].sum()
top_20_percent_contribution = top_20_percent_revenue/total_revenue*100

#observe query result
print("customer_revenue_df", customer_revenue_df) #Always use observe() instead of print
