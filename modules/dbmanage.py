import csv
import pandas as pd
import numpy as np


def dbmanage_load_location_data(database_file=None):
    """
    Load location data and check it with latest tweets
    """
    databaseLocationsDictionary = {}

    with open(database_file, 'r') as f:
        for line in f:
            x = line.split("/")
            x[1] = x[1].replace('\n', '')
            x[1] = x[1].replace(' ', '')
            databaseLocationsDictionary[x[0]] = x[1]

    print(f'Location Database loaded! {len(databaseLocationsDictionary)} entries.\n')

    return databaseLocationsDictionary


def dbmanage_update_csv_data(database=None, dfAppendList=None):
    """
    Input a Pandas dataframe into dfAppend
    """

    dfAppend = pd.DataFrame(dfAppendList, columns=['Date', 'Time', 'Location', 'Latitude', 'Longitude',
                                                   'Direction', 'Type', 'Lanes Blocked', 'Involved', 'Tweet', 'Source'])

    with open(database, mode='a', encoding='utf-8') as f:
        dfAppend.to_csv(f, header=False, index=False)

    df = pd.read_csv(database)
    df.dropna(axis=0, subset=['Source'], inplace=True)
    df.to_csv(database, index=False)


def dbmanage_clean_tweet_data(tweet_database):
    df_1 = pd.read_csv(tweet_database)

    df_1['Longitude'] = df_1['Longitude'].astype(str)
    df_1['Longitude'] = df_1['Longitude'].str.rstrip(' ')
    df_1['Longitude'] = df_1['Longitude'].str.replace('\t', '')
    df_1['Longitude'] = df_1['Longitude'].str.replace('\n', '')
    df_1.replace('None', np.nan, inplace=True)
    df_1.dropna(axis=0, subset=['Source'], inplace=True)
    df_1.to_csv(tweet_database, index=False)


def dbmanage_database_count(tweet_database):
    df = pd.read_csv(tweet_database)
    df_length = len(df)
    return df_length


def dbmanage_check_similar_locations(tweet_location, location_database):
    """
    tweet_location: The location string
    location_database: The file containing the names and coords of locations
    """

    #tweetLocation = 'EDSA ORTIGAS FLYOVER JULIA'

    # Automate getting the word count which will count as the index
    # Split and get word count
    tweetLocationSplit = tweet_location.split(' ')
    search_cap = len(tweetLocationSplit)

    # Create a dictionary of all the individual words/search terms
    search_words = {}
    for x in range(0, search_cap):
        search_words[x] = tweetLocationSplit[x]

    searchOutput_step0 = []
    searchOutput_step1 = []
    searchOutput_step2 = []
    searchOutput_step3 = []
    searchOutput_step4 = []
    searchOutput_step5 = []
    searchOutput_step6 = []
    searchOutput_else = []

    # list of locations from location database
    with open(location_database, 'r') as f:
        line = f.readlines()
        for x in line:
            searchOutput_step0.append(x.split('/')[0])

    for idx in range(0, search_cap):

        searchTerm1 = tweetLocationSplit[0]
        # print('idx {} search_cap {}'.format(idx, search_cap))
        if idx < search_cap-1:
            searchTerm2 = tweetLocationSplit[idx + 1]

        # print('searchTerm1 {} searchTerm2 {}'.format(searchTerm1, searchTerm2))
        counter_hit = 0

        for x in searchOutput_step0:
            if searchTerm1 and searchTerm2 in x:
                counter_hit += 1
                if idx == 0:
                    searchOutput_step1.append(x)
                elif idx == 1:
                    searchOutput_step2.append(x)
                elif idx == 2:
                    searchOutput_step3.append(x)
                elif idx == 3:
                    searchOutput_step4.append(x)
                elif idx == 4:
                    searchOutput_step5.append(x)
                elif idx == 5:
                    searchOutput_step6.append(x)
                else:
                    searchOutput_else.append(x)
        # print('\nBlock {}. Matched {}'.format(idx, counter_hit))

    # search in all the lists
    combinedList = [searchOutput_step1, searchOutput_step2,
                    searchOutput_step3, searchOutput_step4,
                    searchOutput_step5, searchOutput_else]
    locationList = []
    matchDictionary = {}
    matchList = []
    outputList = []

    # Create word list containing output words from all lists
    for group in combinedList:
        if len(group) > 0:
            for location in group:
                locationList.append(location)

    # Create match list where each hit on a word will add 1 to a counter,
    # thus the higher the number the higher the likelihood
    # of it being the ideal match
    for x in locationList:
        if x in matchDictionary:
            matchDictionary[x] += 1
        else:
            matchDictionary[x] = 0

    # Create a list where each item is structured as such:
    # [NUMBER OF HITS LOCATION STRING]
    # This is so the list can be sorted numerically which will show the top hits
    for location in matchDictionary:
        matchList.append('{} {}'.format(matchDictionary[location], location))

    for x in sorted(matchList):
        if int(x[0]) > 1:
            x = x.split(' ')[1]
            x = ' '.join(x)
            outputList.append(x)

        return outputList
