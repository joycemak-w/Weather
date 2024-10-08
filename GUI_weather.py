import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk
import numpy as np
import sqlite3
import pandas as pd

# Initialize Tkinter and Matplotlib Figure
root = tk.Tk()
fig, ax = plt.subplots()

# Tkinter Application
frame = tk.Frame(root)
label = tk.Label(text="Weather Analysis")
label.config(font=("Courier", 32))
label.pack()
frame.pack()

locations_checkboxes = []
filter_var = tk.StringVar()
# filter_options = ['Average temperature per hour', 'Temperature per 5 minutes', 'Different weather count', 'Average humidity per hour', 'Largest temperature difference']
filter_options = ['Average temperature per hour', 'Different weather count', 'Average humidity per hour', 'Largest temperature difference']
filter_combobox = ttk.Combobox(frame, textvariable=filter_var, values=filter_options)
filter_combobox.pack(pady=10)

# Create Canvas
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Plot data on Matplotlib Figure
def filter_data(show_save):
    conn = sqlite3.connect('weather.db')
    cursor = conn.cursor()
    selected_locations = [loc for loc, cb_var in locations_checkboxes if cb_var.get()]
    filter_option = filter_var.get()
    result_text.delete('1.0', tk.END)
    global ax
    ax.clear()  # Clear previous plot
    if filter_option == 'Average temperature per hour':
        df = {}
        for loc in selected_locations:
            sql_query = pd.read_sql_query(f"SELECT AVG(temperature) AS avg_temp,strftime ('%H',timestamp) hour FROM Weathers WHERE location = '{loc}' GROUP BY strftime ('%H',timestamp)",conn)
            df[loc] = pd.DataFrame(sql_query)
        # print(df)
        for loc in selected_locations:
            ax.plot(df[loc]['hour'], df[loc]['avg_temp'], label=loc)

        ax.set_xlabel('Hour')
        ax.set_ylabel('Average Temperature')
        ax.set_title('Location Average Temperature Per Hour')
        ax.legend()
        ax.grid()
        if show_save == 'save':
            fig.savefig('./average_temperature.png')
    # elif filter_option == 'Temperature per 5 minutes':
    #     # t = np.arange(0, 2*np.pi, .01)
    #     # ax.plot(t, np.cos(t))
    #     pass
    elif filter_option == 'Different weather count':
        df = {}
        for loc in selected_locations:
            cursor.execute(f"SELECT weather, count(*) AS count FROM Weathers WHERE location = '{loc}' GROUP BY weather")
            df[loc] = cursor.fetchall()
        # print(df)
        placeholders = ', '.join('?' for _ in selected_locations)
        condition = f"WHERE location IN ({placeholders})" if selected_locations else ""
        query = f'SELECT DISTINCT weather FROM Weathers {condition}'
        cursor.execute(query, selected_locations)
        weather_conditions = cursor.fetchall()
        weather_conditions = [condition[0] for condition in weather_conditions]
        # print(weather_conditions)
        locations = list(df.keys())
        bar_width = 0.15  
        x = np.arange(len(weather_conditions))

        values = np.zeros((len(locations), len(weather_conditions)))

        for i, location in enumerate(locations):
            for condition, count in df[location]:
                if condition in weather_conditions:
                    values[i, weather_conditions.index(condition)] = count

        for i, location in enumerate(locations):
            ax.bar(x + i * bar_width, values[i], width=bar_width, label=location)

        ax.set_xlabel('Weather Conditions')
        ax.set_ylabel('Counts')
        ax.set_title('Weather Conditions Counts by Location')
        ax.set_xticks(x + bar_width / 2, weather_conditions)
        ax.tick_params(axis='x', labelrotation=15)
        ax.legend()
        if show_save == 'save':
            fig.savefig('./weather_count.png')

    elif filter_option == 'Average humidity per hour':
        df = {}
        for loc in selected_locations:
            sql_query = pd.read_sql_query(f"SELECT AVG(humidity) AS avg_temp,strftime ('%H',timestamp) hour FROM Weathers WHERE location = '{loc}' GROUP BY strftime ('%H',timestamp)",conn)
            df[loc] = pd.DataFrame(sql_query)
        for loc in selected_locations:
            ax.plot(df[loc]['hour'], df[loc]['avg_temp'], label=loc)

        ax.set_xlabel('Hour')
        ax.set_ylabel('Average Humidity')
        ax.set_title('Location Average Humidity Per Hour')
        ax.legend()
        ax.grid(True)
        if show_save == 'save':
            fig.savefig('./average_temperature.png')
    elif filter_option == 'Largest temperature difference':
        # results = []
        df = {}          
        for loc in selected_locations:
            sql_query = pd.read_sql_query(f"SELECT MAX(temperature)-MIN(temperature) as diff FROM Weathers WHERE location = '{loc}'",conn)
            df[loc] = pd.DataFrame(sql_query)
        # print(df)
        for location, diff in df.items():
            result_text.insert(tk.END, f'{location}: {diff}\n')
    if filter_option != '' and show_save == 'show':
        canvas.draw()
    elif filter_option != '' and show_save =='save':
        if show_save == 'save':
            df = pd.DataFrame(df.items(), columns=['Location', 'Diff'])
            print(df)
            df.to_csv('./temp_diff.csv')
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, 'Image is downloaded.')
    else:
        result_text.delete('1.0', tk.END)
        result_text.insert(tk.END, 'Data should not be empty.')
    conn.close()

locations = ['Mongolia','Antarctica','Mexicali', 'Taiwan','Hong Kong']
locations_checkboxes = []
for loc in locations:
    cb_var = tk.BooleanVar()
    cb = tk.Checkbutton(frame, text=loc, variable=cb_var)
    cb.pack(anchor='w')
    locations_checkboxes.append((loc, cb_var))

def filter_show():
    filter_data('show')

def filter_save():
    filter_data('save')

show_button = tk.Button(frame, text="Filter", command=filter_show)
show_button.pack(pady=10)

save_button = tk.Button(frame, text="Save Filtered Result", command=filter_save)
save_button.pack(pady=10)

result_text = tk.Text(frame, height=10, width=40)
result_text.pack(pady=20)

filter_data('show')
root.mainloop()