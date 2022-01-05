import pandas as pd

def read_and_clean(filepath):
    """
    Reads in and cleans a csv file to analyze for Netflix watch patterns

    Input:
        filepath (filepath): csv filepath
    
    Returns (pd.dataframe): cleaned dataframe
    """
    data = pd.read_csv(filepath)
    data_reduced = data.drop(['Attributes', 'Supplemental Video Type', 'Bookmark',
                            'Latest Bookmark','Country'], axis = 1)
    data_reduced["Start Time"] =  pd.to_datetime(data_reduced["Start Time"],
                                                utc=True)

    # change the Start Time column into the dataframe's index
    data_utc = data_reduced.set_index('Start Time')
    # convert from UTC timezone to central time
    data_utc.index = data_utc.index.tz_convert('US/Central')
    # reset the index so that Start Time becomes a column again
    data_cst = data_utc.reset_index()

    #Reorder profile back to first
    data_cst = data_cst[['Profile Name', 'Start Time', 'Duration', 'Title', 'Device Type']]

    # convert the duration column to a time delta
    data_cst["Duration"] = pd.to_timedelta(data_cst["Duration"])

    # want only if duration is longer than 30 seconds as don't want to include
    # trailers etc (which Netflix counts as views)
    data_cst = data_cst[ (data_cst["Duration"] > '0 days 00:00:30') ]

    # get show info more organized by splitting title column
    title_info = data_cst["Title"].str.split(":").apply(lambda row: [col.strip() for col in row])
    col_titles = ["Simple Title", "Subtitle", "Season", "Episode"]
    split_show_info = []

    for row in title_info:
        show_data = []
        show_data.append(row[0])
        if len(row) == 2:
            show_data.append(row[1])
            show_data.append("")
            show_data.append("")
            split_show_info.append(show_data)
            continue
        if len(row) > 2:
            if "Season" in row[1]:
                show_data.append("")
                show_data.append(row[1])
                show_data.append(row[2])
                split_show_info.append(show_data)
                continue
            else:
                show_data.append(row[1])
                show_data.append(row[2])
                show_data.append(row[3])
                split_show_info.append(show_data)
                continue
        show_data.append("")
        show_data.append("")
        show_data.append("")
        split_show_info.append(show_data)

    show_info = pd.DataFrame(split_show_info, columns=col_titles)

    detailed_info = pd.concat([data_cst, show_info], axis=1)
    cleaned_info = detailed_info.drop(["Title"], axis = 1)
    final_df = cleaned_info[['Profile Name', 'Start Time', 'Duration', 'Device Type', 'Simple Title', 'Subtitle', 'Season', 'Episode']]
    return final_df

print(read_and_clean("sample_data.csv"))
        
        