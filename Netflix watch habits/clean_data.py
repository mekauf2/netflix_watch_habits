import pandas as pd

def read_and_clean(filepath, profiles=None):
    """
    Reads in and cleans a csv file to analyze for Netflix watch patterns

    Input:
        filepath (filepath): csv filepath
        profile (str): profile name to filter
    
    Returns (pd.dataframe): cleaned dataframe
    """
    data = pd.read_csv(filepath)

    # filter user(s) if given an input
    if profiles:
        try:
            data = data[ (data["Profile Name"].isin(profiles)) ]
        except:
            print("Profile(s) not in dataset")
            exit()

    # remove videos with supplemental video types (these are hooks, recaps,
    # teases, previews, etc.)

    data = data[ (data["Supplemental Video Type"].isnull()) ]

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

    # convert the duration column to a time delta
    data_cst["Duration"] = pd.to_timedelta(data_cst["Duration"])

    # want only if duration is longer than 30 seconds as don't want to include
    # trailers etc (which Netflix counts as views)
    data_cst = data_cst[ (data_cst["Duration"] > '0 days 00:00:30') ]

    # Split up watch start time to make easier to sum
    data_cst["Start Year"] = data_cst["Start Time"].dt.year
    data_cst["Start Day"] = data_cst["Start Time"].dt.day
    data_cst["Start Day of Week"] = data_cst["Start Time"].dt.weekday
    data_cst["Start Hour"] = data_cst["Start Time"].dt.hour
    data_cst["Start Minute"] = data_cst["Start Time"].dt.minute

    # Convert duration into minutes
    data_cst["Duration (min)"] = round(data_cst["Duration"].dt.seconds / 60, 2)
                            # (data_cst["Duration"].dt.hour * 60 +
                            # data_cst["Duration"].dt.minute +
                            # data_cst["Duration"].dt.second / 60)

    # reorder column order
    data_cst = data_cst.drop(["Start Time", "Duration"], axis = 1)
    data_cst = data_cst[['Profile Name', 'Start Year', 'Start Day', 'Start Day of Week', 'Start Hour', 'Start Minute', 'Duration (min)', 'Title', 'Device Type']]

    # get show info more organized by splitting title column
    title_info = data_cst["Title"].str.split(":").apply(lambda row: [col.strip() for col in row])
    title, subtitle, season, episode = [], [], [], []

    for row in title_info:
        title.append(row[0])
        if len(row) == 2:
            subtitle.append(row[1])
            season.append("")
            episode.append("")
            continue
        if "Part " in row[-1] and len(row) > 3: # for episodes such as Manchester: Part I
                row = row[:]
                new_item = row.pop(-2) + ": " + row.pop(-1)
                row.append(new_item)
        if len(row) > 2:    
            # special cases
            if "Book" in row[1]:
                subtitle.append("")
                if "Avatar" in row[0]:
                    season.append(row[1])
                    episode.append(row[2])
                else:
                    season.append(": ".join(row[1:3]))
                    episode.append(row[3])
                continue
            if "Bleach" in row[0]:
                subtitle.append("")
                season.append(row[1])
                episode.append(row[2])
                continue
            if "Comedians in Cars Getting Coffee" == row[0]:
                subtitle.append("")
                if row[1] == "New 2018": # special season
                    row[1] = row[1] + ": " + row.pop(2)
                season.append(row[1])
                episode.append(": ".join(row[2:]))
                continue
            if row[1] == "Black & White":
                subtitle.append(row[1])
                season.append(row[2])
                episode.append(row[4])
                continue
            # general rules
            if "Season" in row[1] or "Part" in row[1] or "Volume" in row[1]:
                subtitle.append("")
                season.append(row[1])
                episode.append(row[2])
                continue
            elif len(row) == 3:
                subtitle.append(row[1])
                season.append("")
                episode.append(row[2])
                continue
            elif len(row) == 4:
                subtitle.append(row[1])
                season.append(row[2])
                episode.append(row[3])
                continue
        # movie or some other thing of 1 item length
        subtitle.append("")
        season.append("")
        episode.append("")

    base_df = data_cst.drop(["Title"], axis = 1)
    final_df = base_df.assign(Title = title,
                              Subtitle = subtitle,
                              Season = season,
                              Episode = episode)
    
    final_df.to_csv(r"C:\Users\matth\OneDrive\Documents\Coding Projects\Netflix watch habits\output.csv", index=False)
    return final_df

if __name__ == "__main__":
    file_path = input("What filepath should we clean? \n").strip()
    try:
        f = open(file_path)
    except:
        print("path invalid, try a different path")
        exit()

    user_question = "\nWhat user should we focus on?\n"
    user_detail = "Please ener profile name(s) seperated by a comma and space \
        or 'None' to look at all users)\n"

    user_input = input(f"{user_question}{user_detail}")
    users = list(user_input.split(", "))
    try:
        read_and_clean(file_path, users)
    except:
        print(f"users entered {users}")
