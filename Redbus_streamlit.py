import streamlit as st
import pymysql
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime
# Function to fetch and display bus details with filters for price, star rating, bus type, and time
def fetch_and_display_bus_details(route_name, price_range_query, min_star_rating, max_star_rating, selected_bus_types, start_time, end_time):
    conn = pymysql.connect(host="localhost", user="root", password="14201420vj", database="redbus_details")
    my_cursor = conn.cursor()
    query = f'''SELECT * FROM redbus_details.bus_routedetails 
                WHERE {price_range_query} 
                AND Star_rating >= {min_star_rating} 
                AND Star_rating <= {max_star_rating}
                AND Route_name = "{route_name}"
                AND Departing_time >= "{start_time}" 
                AND Departing_time <= "{end_time}"
                '''
    if selected_bus_types:
        bus_types_condition = " OR ".join([f'Bus_type = "{bus_type}"' for bus_type in selected_bus_types])
        query += f" AND ({bus_types_condition})" 
    query += " ORDER BY price DESC" 
    my_cursor.execute(query)
    out = my_cursor.fetchall()
    conn.close()  
    df = pd.DataFrame(out, columns=["Route_name", "Route_link", "Bus_name", "Bus_type", "Departing_time", "Duration", "Reach_time", 
                                    "Star_rating", "price", "Seat_available"])
    st.write(df)
def load_routes(file_path):
    df = pd.read_csv(file_path)
    return df["Route_name"].tolist()
lists_A = load_routes(r"C:\Users\vasan\Desktop\route\route1.csv")  # Andhra Pradesh
lists_K = load_routes(r"C:\Users\vasan\Desktop\route\route2.csv")  # Kerala
lists_T = load_routes(r"C:\Users\vasan\Desktop\route\route3.csv")  # Telangana
lists_R = load_routes(r"C:\Users\vasan\Desktop\route\route4.csv")  # Rajasthan
lists_S = load_routes(r"C:\Users\vasan\Desktop\route\route5.csv")  # South Bengal
lists_H = load_routes(r"C:\Users\vasan\Desktop\route\route6.csv")  # Himachal
lists_U = load_routes(r"C:\Users\vasan\Desktop\route\route7.csv")  # Uttar Pradesh
lists_W = load_routes(r"C:\Users\vasan\Desktop\route\route8.csv")  # West Bengal (CTC)
lists_P = load_routes(r"C:\Users\vasan\Desktop\route\route9.csv")  # Punjab
lists_WB = load_routes(r"C:\Users\vasan\Desktop\route\route10.csv")  # WBSTC
state_routes = {"Andhra Pradesh": lists_A,"Kerala": lists_K,"Telangana": lists_T,"Rajasthan": lists_R,"South Bengal": lists_S,
"Himachal": lists_H,"Uttar Pradesh": lists_U,"West Bangal(CTC)": lists_W,"Panjab": lists_P,"WBSTC": lists_WB}
bus_types = ["Volvo 9600 Multi-Axle A/C Sleeper (2+1)","A/C Seater / Sleeper (2+1)","NON A/C Semi Sleeper / Sleeper (2+1)","A/C Sleeper (2+1)",
    "Scania AC Multi Axle Sleeper (2+1)","Volvo Multi-Axle A/C Sleeper (2+1)","Bharat Benz A/C Sleeper (2+1)","Non A/C Seater / Sleeper (2+1)",
    "VE A/C Seater / Sleeper (2+1)","Scania Multi-Axle AC Seater (2+2)","NON A/C Sleeper (2+1)"]
st.set_page_config(layout="wide")
web = option_menu(menu_title="🔴OnlineBus🚌",
                 options=["🏡Home", "📌States and Routes"],
                 icons=[":house:", "info-circle"],
                 orientation="horizontal"
                 )
if web == "🏡Home":
    st.image(r"C:\Users\vasan\Pictures\Redbus_logo.jpg", width=200)
    st.title(":red[Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit]")
    st.video(r"C:\Users\vasan\Pictures\redBus_Hire___Product_Video(1080p).mp4")
    st.image(r"C:\Users\vasan\Pictures\Screenshots\redbuslogo.png", width=200)
    st.markdown("[⬇️Download Redbus app](https://play.google.com/store/apps/details?id=in.redbus.android&hl=en_IN&pli=1)")
    st.subheader(":red[Domain:] Transportion")
    st.subheader(":red[Objective: ]")
    st.markdown(" The 'Redbus Data Scraping and Filtering with Streamlit Application' aims to revolutionize the transportation industry by providing a comprehensive solution for collecting, analyzing, and visualizing bus travel data. By utilizing Selenium for web scraping, this project automates the extraction of detailed information from Redbus, including bus routes, schedules, prices, and seat availability.")
    st.subheader(":red[Overview: ]")
    st.markdown("selenium : selenium is a tool used for automating web browsers. It is commonly used for web scraping, which involves extracting data from websites.")
    st.markdown("Pandas : Pandas is a popular open-source library in Python for data manipulation and analysis. It provides data structures and tools to efficiently handle and process structured data, such as datasets stored in spreadsheets or databases. Pandas is built on top of NumPy, and it is widely used in data science, machine learning, and statistical analysis.")
    st.markdown("MySQL : MySQL is an open-source relational database management system (RDBMS) that uses Structured Query Language (SQL) for managing and manipulating data. It is widely used in web applications, data storage, and analytics due to its speed, reliability, and ease of use.")
    st.markdown("Streamlit : Streamlit is an open-source Python library designed for creating interactive, data-driven web applications with ease. It is widely used in data science and machine learning projects to build dashboards and visualization tools. Streamlit simplifies the process of turning Python scripts into web apps without requiring extensive knowledge of web development frameworks like HTML, CSS, or JavaScript.")
    st.subheader(":red[Skill-taken:]") 
    st.markdown("selenium, python, pandas, MYSQL,mysql-connector-python,Streamlit.")
    st.subheader(":red[Developed-by:] G.Vasanth Raj")
if web == "📌States and Routes":
    s = st.selectbox("List of States", list(state_routes.keys()))
    select_fare = st.radio("Choose bus fare range", ("40-1000", "1000-2000", "2000 and above"))
    min_star_rating = st.slider("Minimum Star Rating", min_value=1, max_value=5, value=1, step=1)
    max_star_rating = st.slider("Maximum Star Rating", min_value=1, max_value=5, value=5, step=1)
    selected_bus_types = st.multiselect("Select Bus Types", bus_types, default=bus_types)
    start_time = st.time_input("Start Time", value=datetime(2000, 1, 1, 6, 0, 0).time())  # Default to 6:00 AM
    end_time = st.time_input("End Time", value=datetime(2000, 1, 1, 23, 59, 59).time())  # Default to 11:59 PM
    if s in state_routes:
        selected_routes = state_routes[s]
        A = st.selectbox("List of routes", selected_routes) 
        if select_fare == "40-1000":
            price_range_query = "price BETWEEN 40 AND 1000"
        elif select_fare == "1000-2000":
            price_range_query = "price BETWEEN 1000 AND 2000"
        elif select_fare == "2000 and above":
            price_range_query = "price > 2000"
        fetch_and_display_bus_details(A, price_range_query, min_star_rating, max_star_rating, selected_bus_types, start_time, end_time)
