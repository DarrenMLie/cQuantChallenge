# Import libraries
import pandas as pd
import matplotlib.pyplot as plt

# Improvements (couldn't get to these because I ran out of time):
# 1. Refactor code to be more modular (use functions and loops)
# 2. Create better visualization of data
# 3. Generate additional tables and groupings of data
# 4. Calculate additional statistics about the data (variance, standard deviation, etc)

# Import datasets (Task 1)
dfA = pd.read_csv("data/PriceData_A.csv")
dfB = pd.read_csv("data/PriceData_B.csv")

# Reshape datasets from wide to long (Task 2)
dfA_long = pd.melt(dfA, id_vars=['Name', 'Date'], value_vars=['Run_1', 'Run_2', 'Run_3', 'Run_4', 'Run_5'],
                   var_name='Run', value_name='Value')
dfB_long = pd.melt(dfB, id_vars=['Name', 'Date'], value_vars=['Run_1', 'Run_2', 'Run_3', 'Run_4', 'Run_5'],
                   var_name='Run', value_name='Value')

# Join datasets on Name, Date, and Run columns and rename column names (Task 3)
cols = ['Name', 'Date', 'Run']
merged_df = pd.merge(dfA_long, dfB_long, on=cols)
merged_df.rename(columns = {'Value_x':'Value_A', 'Value_y':'Value_B'}, inplace = True)

# Obtain the difference metrics between the two datasets (Task 4)
merged_df_diff = merged_df.copy()
merged_df_diff["Difference"] = merged_df["Value_A"] - merged_df["Value_B"]
merged_df_diff["Percent_Difference"] = (merged_df["Value_A"] - merged_df["Value_B"]) / merged_df["Value_A"] 
merged_df_diff["Absolute_Difference"] = abs(merged_df["Value_A"] - merged_df["Value_B"])
merged_df_diff["Absolute_Percent_Difference"] = abs((merged_df["Value_A"] - merged_df["Value_B"]) / merged_df["Value_A"])

# Obtaining the statistics of the absolute difference metric in part grouped by different time and date dimensions (Task 5)
# Parse relevant time and date dimensions so we can use them to groupdata
merged_df_diff['Date'] = pd.to_datetime(merged_df_diff['Date'])
merged_df_diff['Year'] = merged_df_diff['Date'].dt.year
merged_df_diff['Month'] = merged_df_diff['Date'].dt.month
merged_df_diff['Day_Of_Week'] = merged_df_diff['Date'].dt.dayofweek
merged_df_diff['Hour_Of_Day'] = merged_df_diff['Date'].dt.hour

# Create dataframe to group data by year
df_stats_year = pd.DataFrame()
df_stats_year["Min"] = merged_df_diff.groupby('Year')['Absolute_Difference'].min()
df_stats_year["Max"] = merged_df_diff.groupby('Year')['Absolute_Difference'].max()
df_stats_year["Mean"] = merged_df_diff.groupby('Year')['Absolute_Difference'].mean()
df_stats_year = df_stats_year.reset_index()

# Create dataframe to group data by month
df_stats_month = pd.DataFrame()
df_stats_month["Min"] = merged_df_diff.groupby('Month')['Absolute_Difference'].min()
df_stats_month["Max"] = merged_df_diff.groupby('Month')['Absolute_Difference'].max()
df_stats_month["Mean"] = merged_df_diff.groupby('Month')['Absolute_Difference'].mean()
df_stats_month = df_stats_month.reset_index()

# Create dataframe to group data by day of week
df_stats_day_of_week = pd.DataFrame()
df_stats_day_of_week["Min"] = merged_df_diff.groupby('Day_Of_Week')['Absolute_Difference'].min()
df_stats_day_of_week["Max"] = merged_df_diff.groupby('Day_Of_Week')['Absolute_Difference'].max()
df_stats_day_of_week["Mean"] = merged_df_diff.groupby('Day_Of_Week')['Absolute_Difference'].mean()
df_stats_day_of_week = df_stats_day_of_week.reset_index()

# Create dataframe to group data by hour of day
df_stats_hour_of_day = pd.DataFrame()
df_stats_hour_of_day["Min"] = merged_df_diff.groupby('Hour_Of_Day')['Absolute_Difference'].min()
df_stats_hour_of_day["Max"] = merged_df_diff.groupby('Hour_Of_Day')['Absolute_Difference'].max()
df_stats_hour_of_day["Mean"] = merged_df_diff.groupby('Hour_Of_Day')['Absolute_Difference'].mean()
df_stats_hour_of_day = df_stats_hour_of_day.reset_index()

# Export all data to .csv format (Task 6)
df_stats_year.to_csv("Absolute_Difference_Statistics_Year.csv")
df_stats_month.to_csv("Absolute_Difference_Statistics_Month.csv")
df_stats_day_of_week.to_csv("Absolute_Difference_Statistics_Day_Of_Week.csv")
df_stats_hour_of_day.to_csv("Absolute_Difference_Statistics_Hour_Of_Day.csv")

# Create plots to describe differences in data (Task 7)
# Plot for the absolute difference by year
plt.plot(df_stats_year['Year'], df_stats_year['Min'], label='Min')
plt.plot(df_stats_year['Year'], df_stats_year['Max'], label='Max')
plt.plot(df_stats_year['Year'], df_stats_year['Mean'], label='Mean')
plt.xticks(df_stats_year['Year'],["2024","2025","2026"])
plt.xlabel('Year')
plt.ylabel('Absolute Price Difference')
plt.title("Absolute Price Difference Statistics Between A and B By Year")
plt.legend()
# plt.show()
plt.savefig("Absolute_Difference_Statistics_Year.png")

# Plot for the absolute difference by month
plt.plot(df_stats_month['Month'], df_stats_month['Min'], label='Min')
plt.plot(df_stats_month['Month'], df_stats_month['Max'], label='Max')
plt.plot(df_stats_month['Month'], df_stats_month['Mean'], label='Mean')
plt.xticks(df_stats_month['Month'],
           ["January","February","March", "April","May","June","July","August","September","October","November","December"],
           rotation=45)
plt.xlabel('Month')
plt.ylabel('Absolute Price Difference')
plt.title("Absolute Price Difference Statistics Between A and B By Month")
plt.legend()
# plt.show()
plt.savefig("Absolute_Difference_Statistics_Month.png")

# Plot for the absolute difference by day of week
plt.plot(df_stats_day_of_week['Day_Of_Week'], df_stats_day_of_week['Min'], label='Min')
plt.plot(df_stats_day_of_week['Day_Of_Week'], df_stats_day_of_week['Max'], label='Max')
plt.plot(df_stats_day_of_week['Day_Of_Week'], df_stats_day_of_week['Mean'], label='Mean')
plt.xticks(df_stats_day_of_week['Day_Of_Week'],
           ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
           rotation=22.5)
plt.xlabel('Day_Of_Week')
plt.ylabel('Absolute Price Difference')
plt.title("Absolute Price Difference Statistics Between A and B By Day Of Week")
plt.legend()
# plt.show()
plt.savefig("Absolute_Difference_Statistics_Day_Of_Week.png")

# Plot for the absolute difference by hour of day
plt.plot(df_stats_hour_of_day['Hour_Of_Day'], df_stats_hour_of_day['Min'], label='Min')
plt.plot(df_stats_hour_of_day['Hour_Of_Day'], df_stats_hour_of_day['Max'], label='Max')
plt.plot(df_stats_hour_of_day['Hour_Of_Day'], df_stats_hour_of_day['Mean'], label='Mean')
plt.xticks(df_stats_hour_of_day['Hour_Of_Day'],
           ["00:00","01:00","02:00","03:00","04:00","05:00","06:00","07:00","08:00","09:00","10:00","11:00",
            "12:00","13:00","14:00","15:00","16:00","17:00","18:00","19:00","20:00","21:00","22:00","23:00"],
           rotation=45)
plt.xlabel('Hour Of Day')
plt.ylabel('Absolute Price Difference')
plt.title("Absolute Price Difference Statistics Between A and B by Hour Of Day")
plt.legend()
# plt.show()
plt.savefig("Absolute_Difference_Statistics_Hour_Of_Day.png")