import matplotlib.pyplot as plt
from numpy import datetime_data
import seaborn as sns
import pandas as pd

sns.set_style('darkgrid') # darkgrid, white grid, dark, white and ticks
colors = sns.color_palette("dark") # set color pallete
plt.rc('axes', titlesize=18)     # fontsize of the axes title
plt.rc('axes', labelsize=12)    # fontsize of the x and y labels
plt.rc('xtick', labelsize=9)    # fontsize of the tick labels
plt.rc('ytick', labelsize=9)    # fontsize of the tick labels
plt.rc('legend', fontsize=12)    # legend fontsize
plt.rc('font', size=12)          # controls default text sizes
plt.figure(figsize=(8,4), tight_layout=True) # size of plot

DAY_NAMES = {0:'Mon', 1:'Tue', 2:'Wed', 3:'Thu', 4:'Fri', 5:'Sat', 6:'Sun'}
MONTH_NAMES = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
               7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
COLUMNS_TIME_DICT = {"year": 'Start Year', "month": 'Start Month', 
                     "day of month": 'Start Day', "day of week": 'Start Day of Week',
                     "hour of day": 'Start Hour'}

def find_time_watched(filepath, time_unit="year", start_year=None):
    """
    Reads in a clean csv file to analyze total Netflix watched

    Input:
        filepath (filepath): csv filepath
        time_unit (str): time_unit to slice data on
        start_year (int): start year for data analysis
    
    Returns (plt bar graph): bar graph of time spent on Netflix
    """
    data = pd.read_csv(filepath)

    assert time_unit in ["year", "month", "day of week", "day of month", "hour of day"], \
        print("Pick a different time unit")

    min_year = min(data["Start Year"].unique())
    if start_year:
        assert start_year >= min_year, print("Pick a different start year")
        data = data[ (data["Start Year"] >= start_year) ]
    else:
        start_year = min_year

    col_to_use = COLUMNS_TIME_DICT[time_unit]

    data_to_use = data[[col_to_use, "Duration (min)"]]
    barplot = data_to_use.groupby(col_to_use).sum().reset_index()
    
    barplot = barplot.sort_values(by = col_to_use)


    if time_unit == "month":
        barplot[col_to_use] = barplot[col_to_use].map(MONTH_NAMES)
    if time_unit == "day of week":
        barplot[col_to_use] = barplot[col_to_use].map(DAY_NAMES)

    plt.bar(barplot[col_to_use], barplot["Duration (min)"], color=colors[0])
    plt.title("Netflix watch time by " + time_unit + " since " + str(start_year))
    plt.ylabel("Minutes watched") 

    return plt.show()

def find_average_time_watched(filepath, time_unit="year", start_year=None):
    """
    Reads in a clean csv file to analyze average Netflix watched

    Input:
        filepath (filepath): csv filepath
        time_unit (str): time_unit to slice data on
        start_year (int): start year for data analysis
    
    Returns (plt bar graph): bar graph of average time spent on Netflix
    """
    data = pd.read_csv(filepath)

    assert time_unit in ["year", "month", "day of week", "day of month", "hour of day"], \
        print("Pick a different time unit")

    min_year = min(data["Start Year"].unique())
    if start_year:
        assert start_year >= min_year, print("Pick a different start year")
        data = data[ (data["Start Year"] >= start_year) ]
    else:
        start_year = min_year

    col_to_use = COLUMNS_TIME_DICT[time_unit]

    data_to_use = data[[col_to_use, "Duration (min)"]]
    barplot = data_to_use.groupby(col_to_use).mean().reset_index()
    
    barplot = barplot.sort_values(by = col_to_use)

    if time_unit == "month":
        barplot[col_to_use] = barplot[col_to_use].map(MONTH_NAMES)
    if time_unit == "day of week":
        barplot[col_to_use] = barplot[col_to_use].map(DAY_NAMES)

    plt.bar(barplot[col_to_use], barplot["Duration (min)"], color=colors[0])
    plt.title("Average Netflix watch time per session by " + time_unit + " since " + str(start_year))
    plt.ylabel("Minutes watched")    

    return plt.show()

def find_max_binges(filepath, number_binges=10, start_year=None):
    """
    Reads in a clean csv file to analyze top binge lengths

    Input:
        filepath (filepath): csv filepath
        number_binges (int): top binges to display
        start_year (int): start year for data analysis
    
    Returns (plt bar graph): bar graph of top binges watched on Netflix
    """
    data = pd.read_csv(filepath)

    min_year = min(data["Start Year"].unique())
    if start_year:
        assert start_year >= min_year, print("Pick a different start year")
        data = data[ (data["Start Year"] >= start_year) ]
    else:
        start_year = min_year

    data_to_use = data[["Title", "Binge (min)", "Start Year", "Start Month", "Start Day"]]
    data_to_use.rename(columns={"Start Year": "year", "Start Month": "month", "Start Day": "day"}, inplace=True)
    data_to_use["Date"] = pd.to_datetime( data_to_use[["year", "month", "day"]] )
    data_to_use.drop(["year", "month", "day"], axis=1, inplace=True)
    barplot = data_to_use.sort_values(by="Binge (min)", ascending=False)
    barplot = barplot[:number_binges]
    barplot["Date"] = barplot["Date"].astype(str)
    barplot["Label"] = barplot[["Title", "Date"]].agg("\n".join, axis=1)

    plt.bar(barplot["Label"], barplot["Binge (min)"], color=colors[0])
    plt.title("Top " + str(number_binges) + " Netflix binges by time since " + str(start_year))
    plt.ylabel("Minutes watched")
    plt.xlabel("Binge date and show")

    return plt.show()

def find_time_watched_by_show(filepath, number_shows=10, start_year=None):
    """
    Reads in a clean csv file to analyze total Netflix watched by show

    Input:
        filepath (filepath): csv filepath
        number_shows (int): top shows to display
        start_year (int): start year for data analysis
    
    Returns (plt bar graph): bar graph of top shows watched on Netflix
    """
    data = pd.read_csv(filepath)

    min_year = min(data["Start Year"].unique())
    if start_year:
        assert start_year >= min_year, print("Pick a different start year")
        data = data[ (data["Start Year"] >= start_year) ]
    else:
        start_year = min_year

    data_to_use = data[["Title", "Duration (min)"]]
    barplot = data_to_use.groupby("Title").sum().reset_index()
    barplot = barplot.sort_values(by="Duration (min)", ascending=False)
    barplot = barplot[:number_shows]

    plt.bar(barplot["Title"], barplot["Duration (min)"], color=colors[0])
    plt.title("Top " + str(number_shows) + " Netflix shows watched by time since " + str(start_year))
    plt.ylabel("Minutes watched")    

    return plt.show()

def find_data_by_time_frame(filepath, time_unit="year", start_year=None, dur_type="show"):
    """
    Reads in a clean csv file to find top show or binge in a certain timeframe

    Input:
        filepath (filepath): csv filepath
        time_unit (str): time_unit to slice data on
        start_year (int): start year for data analysis
        dur_type(str): what to find (show or binge)
    
    Returns (plt bar graph): bar graph of top show or binge by timeframe spent on Netflix
    """
    data = pd.read_csv(filepath)

    assert time_unit in ["year", "month", "day of week", "day of month", "hour of day"], \
        print("Pick a different time unit")
    
    assert dur_type in ["show", "binge"], print("Needs to be show or binge")

    years = data["Start Year"].unique()
    min_year = min(years)
    if start_year:
        assert start_year >= min_year, print("Pick a different start year")
        data = data[ (data["Start Year"] >= start_year) ]
    else:
        start_year = min_year

    time_col = COLUMNS_TIME_DICT[time_unit]
    times = data[time_col].unique()

    if dur_type == "show":
        duration_col = "Duration (min)"
    else:
        duration_col = "Binge (min)"    

    data_to_use = data[[time_col, duration_col, "Title"]]
    barplot = pd.DataFrame(columns=[time_col, duration_col, "Title"])
    for time in times[::-1]:
        df = data_to_use[ (data_to_use[time_col] == time) ]
        if dur_type == "show":
            df = df.groupby(["Title", time_col]).sum().reset_index()
        maximum_duration = max(df[duration_col])
        max_row = df[ (df[duration_col] == maximum_duration)]
        barplot = barplot.append(max_row, ignore_index=True)

    barplot = barplot.sort_values(by = time_col)

    if time_unit == "month":
        barplot[time_col] = barplot[time_col].map(MONTH_NAMES)
    if time_unit == "day of week":
        barplot[time_col] = barplot[time_col].map(DAY_NAMES)
    
    barplot[time_col] = barplot[time_col].astype(str)

    barplot["Label"] = barplot[[time_col, "Title"]].agg("\n".join, axis=1)

    plt.bar(barplot["Label"], barplot[duration_col], color=colors[0])
    plt.title("Top " + dur_type + " by " + time_unit + " since " + str(start_year))
    plt.ylabel("Minutes watched")    

    return plt.show()

if __name__ == "__main__":
    filepath = input("What cleaned up file should we make a graph from? \n").strip()
    try:
        f = open(filepath)
    except:
        print("path invalid, try a different path")
        exit()

    user_question = "\nWhat analysis should we focus on:\n"
    user_detail_1 = "Total time watched, average time watched, watch time by show, max binges, or top show by binge / watch per unit of time (e.g. by year)?"
    user_detail_2 = "\nPlease enter total, average, show, binge, or top shows\n"

    desired_analysis = input(f"{user_question}{user_detail_1}{user_detail_2}").strip().lower()
    while desired_analysis not in ["total", "average", "show", "binge", "top shows"]:
        print("cannot run this analysis, please select again")
        desired_analysis = input(f"{user_question}{user_detail_1}{user_detail_2}").strip().lower()

    data = pd.read_csv(filepath)
    min_year = min(data["Start Year"].unique())

    time_unit_prompt = "please select a time unit from the following:"
    time_options = ["year", "month", "day of week", "day of month", "hour of day"]

    show_prompt = "Please select the number of top-watched shows you want shown (less than or equal to "
    binge_prompt = "Please select the number of longest binges you want shown (less than or equal to "

    top_show_prompt = "Pick between most watched show or longest binge.\nPlease pick between: "
    top_show_options = ["show", "binge"]

    start_year_prompt = "please select a start year for analysis greater than or equal to "

    start_year = input(f"{start_year_prompt}{min_year}\n")
    while not start_year.isdigit():
        print("Please enter an integer \n")
        start_year = input(f"{start_year_prompt}{min_year}\n")
    start_year = int(start_year)
    while start_year < min_year:
        print("Invalid year \n")
        start_year = input(f"{start_year_prompt}{min_year}\n")
        while not start_year.isdigit():
            print("Please enter an integer \n")
            start_year = input(f"{start_year_prompt}{min_year}\n")
        start_year = int(start_year)

    if desired_analysis in ["total", "average"]:
        time_input = input(f"{time_unit_prompt}\n{time_options}\n")
        while time_input not in time_options:
            print("Invalid selection \n")
            time_input = input(f"{time_unit_prompt}\n{time_options}\n")
        if desired_analysis == "total":
            find_time_watched(filepath, time_input, start_year)
        else:
            find_average_time_watched(filepath, time_input, start_year)
    elif desired_analysis == "binge":
        max_binges = len(data["Binge (min)"].unique())
        number_binges = input(f"{binge_prompt}{max_binges})\n")
        while not number_binges.isdigit():
            print("Please enter an integer greater than 0 \n")
            number_binges = input(f"{binge_prompt}{max_binges})\n")
        number_binges = int(number_binges)
        while number_binges > max_binges or number_binges < 1:
            print("Invalid number of shows \n")
            number_binges = input(f"{show_prompt}{max_binges})\n")
            while not number_binges.isdigit():
                print("Please enter an integer \n")
                number_binges = input(f"{show_prompt}{max_binges})\n")
            number_binges = int(number_binges)
        find_max_binges(filepath, number_binges, start_year)
    elif desired_analysis == "top shows":
        time_input = input(f"{time_unit_prompt}\n{time_options}\n")
        while time_input not in time_options:
            print("Invalid selection \n")
            time_input = input(f"{time_unit_prompt}\n{time_options}\n")
        dur_type = input(f"{top_show_prompt}\n{top_show_options}\n")
        while dur_type not in top_show_options:
            print("Invalid selection \n")
            dur_type = input(f"{top_show_prompt}\n{top_show_options}\n")
        find_data_by_time_frame(filepath, time_input, start_year, dur_type)
    else:
        max_shows = len(data["Title"].unique())
        number_shows = input(f"{show_prompt}{max_shows})\n")
        while not number_shows.isdigit():
            print("Please enter an integer greater than 0 \n")
            number_shows = input(f"{show_prompt}{max_shows})\n")
        number_shows = int(number_shows)
        while number_shows > max_shows or number_shows < 1:
            print("Invalid number of shows \n")
            number_shows = input(f"{show_prompt}{max_shows})\n")
            while not number_shows.isdigit():
                print("Please enter an integer \n")
                number_shows = input(f"{show_prompt}{max_shows})\n")
            number_shows = int(number_shows)
        find_time_watched_by_show(filepath, number_shows, start_year)