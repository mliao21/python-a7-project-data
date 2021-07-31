# project_data.py
# AUTHOR NAME: Melissa Liao
#
# A terminal-based application for computing and printing statistics based on given input. Four different datasets will be merged into one to compute
# statistics about a country, its subregion and region. The datasets are generally about the usage of cellphones, internet and population growth of each country. 
# User input is required to calculate the statistics. Follow along the instructions given in the terminal as you go. 
# 
import numpy as np
import pandas as pd
from pandas.core.reshape.merge import merge
import matplotlib.pyplot as plt

def country_stats(data, country):
    """ Function prints out information about the country input by user.

        Parameters: the main merged dataset is needed and the chosen country. It slices a sub-array from the main data and filters it 
        by the country input by the user.

        Returns: it returns to the total population, the number of cellphones per 100 people and the percentage of internet users in
        year 2005, 2010 and 2015 of a given country. It also prints out the country's sub-region and region it belongs to.
    """ 
    # A sub-set of the data is sliced to look for the country's sub-region and region.
    country_data = data.loc[pd.IndexSlice[:, :, country]]
    chosen_subreg = country_data.index.get_level_values('UN Sub-Region').values
    print('\nCountry:', country, ' UN Sub-Region:', chosen_subreg, ' UN Region:', country_data.index.get_level_values('UN Region').values)
    
    # Prints out the values of year 2005 in population, cellphone and internet usage.
    print('Year 2005: Population =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2005_pop']].values), '',
          'Cellphones per 100 People =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2005_c%']].values), 
          'Internet Users =', data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2005_i%']].values, '%')

    # Prints out the values of year 2010 in population, cellphone and internet usage.
    print('Year 2010: Population =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2010_pop']].values), '',
          'Cellphones per 100 People =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2010_c%']].values), '',
          'Internet Users =', data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2010_i%']].values, '%')

    # Prints out the values of year 2015 in population, cellphone and internet usage.
    print('Year 2015: Population =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2015_pop']].values), '',
           'Cellphones per 100 People =', int(data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2015_c%']].values), '',
           'Internet Users =', data.loc[pd.IndexSlice[:, :, country], pd.IndexSlice['2015_i%']].values, '%')


def subreg_stats(data, country):
    """ Function prints out information about the sub-region which the country belongs to.

        Parameters: the main merged dataset is needed and the chosen country. It slices a sub-array from the main data and filters it 
        by the country input by the user.

        Returns: it returns to the total population, the average number of cellphone per 100 people and the average percentage of 
        internet users of the sub-region in year 2015.       
    """ 
    # A sub-set of the data is sliced to look for the country's sub-region data.
    country_data = data.loc[pd.IndexSlice[:, :, country]]
    chosen_subreg = country_data.index.get_level_values('UN Sub-Region').values
    # Population in 2015 is added for all countries within the same sub-region.
    subreg_popsum = data.groupby('UN Sub-Region')['2015_pop'].sum()
    # The average of cellphone and internet usage in 2015 within the sub-region is calculated using pivot table.
    avg_subreg = data.pivot_table(index = 'UN Sub-Region', aggfunc = {'2015_c%':'mean', '2015_i%':'mean'})

    # Prints out the brief summary information about the sub-region.
    print('\nSummary of Sub-Region in 2015:')
    print('Total Population =', int(subreg_popsum[chosen_subreg]))
    print('Avg Cellphone per 100 People =', int(avg_subreg.loc[pd.IndexSlice[chosen_subreg], pd.IndexSlice['2015_c%']].values))
    print('Avg Internet Users =', int(avg_subreg.loc[pd.IndexSlice[chosen_subreg], pd.IndexSlice['2015_i%']].values), '%')


def region_cell_int_info(data):
    """ Function plots out the trend of the average cellphone and internet usage for each region.

        Parameters: it needs the main data set to plot out the entire data. From there, it takes a sub-array of all years in the
        number of cellphones per 100 people and the percentage of internet users.

        Returns: it returns to two subplots graphs of each trend data type for each region to compare if there's any correlation
        between those two sub-dataset across 2005, 2010 and 2015.
    """ 
    # Calculates the average cellphone and internet usage for each region
    avg_cell_per_reg = data.pivot_table(index = 'UN Region', aggfunc = {'Number of cellphones per 100 people in 2005':'mean', 'Number of cellphones per 100 people in 2010':'mean', 'Number of cellphones per 100 people in 2015':'mean'})
    avg_int_per_reg = data.pivot_table(index = 'UN Region', aggfunc = {'% Internet users in 2005':'mean', '% Internet users in 2010':'mean', '% Internet users in 2015':'mean'})

    # Set plotting layout and labels from the sub-dataset
    plt.figure(1)
    compare_cellphone_internet = plt.figure(1)
    (top, bottom) = compare_cellphone_internet.subplots(2)
    compare_cellphone_internet.suptitle('Cellphones vs Internet Usage Trend')
    top.plot(avg_cell_per_reg)
    bottom.plot(avg_int_per_reg)
    top.set(xlabel = 'Region', ylabel = 'Cellphones Usage %')
    bottom.set(xlabel = 'Region', ylabel = 'Internet Usage %')
    top.set_title('Data for Cellphones Usage')
    bottom.set_title('Data for Internet Usage')
    top.legend(['2005', '2010','2015'])
    bottom.legend(['2005', '2010','2015'])
    plt.show()


def main():

    print('\n***ENSF 592 Project Data***')
    # Merged two different files into one. I filtered both data to only use the country column and years 2005, 2010, 2015.
    percent_cellphones = pd.read_excel(r".\Country Tech Use\num_cell_phones_per_100_people.xlsx", index_col = [0], usecols = [0,31,36,41])
    total_cellphones = pd.read_excel(r".\Country Tech Use\total_cell_phones_by_country.xlsx", index_col = [0], usecols = [0,31,36,41])
    cellphones_data = pd.merge(percent_cellphones, total_cellphones, how='outer', left_index=True, right_index=True, suffixes=['_c%', '_c#'])
     
    percent_internet = pd.read_excel(r".\Country Tech Use\percentage_population_internet_users.xlsx", index_col = [0], usecols = [0,31,36,41])
    population_data = pd.read_excel(r".\UN Population Datasets\UN Population Dataset 1.xlsx", index_col = [1,2,3]).drop('Code', axis = 1)
    # Filtered the population_data by the population annual rate of increase.
    pop_filtered = population_data.loc[pd.IndexSlice[:, :, 'Population annual rate of increase (percent)']].unstack()
    # Cleaned out the years that were not relevant to my merging data and only kept with years 2005, 2010, and 2015.
    pop_cleaned = pd.DataFrame(pop_filtered.values, index = pop_filtered.index, columns = pop_filtered.columns.droplevel(0)).drop(2000, axis = 1)
    # Left merged the percent_internet data with cleaned population data to filter and keep countries only (sub-regions/regions are excluded).
    internet_pop_data = pd.merge(percent_internet, pop_cleaned, how='left', left_index=True, right_index=True, suffixes=['_i%', '_r'])

    # Merged all the data into one and set its index with 3 levels.
    combined_data = pd.concat([cellphones_data, internet_pop_data], axis=1)
    countries_info = pd.read_excel(r".\UN Population Datasets\UN Codes.xlsx")
    project_data = pd.merge(countries_info, combined_data, how='outer', left_on='Country', right_index=True).set_index(['UN Region', 'UN Sub-Region', 'Country']).sort_index()

    # Added three columns to the main merged dataset to calculate the total population per country and per year.
    project_data['2005_pop'] = project_data['2005_c#'] / (project_data['2005_c%'] / 100)
    project_data['2010_pop'] = project_data['2010_c#'] / (project_data['2010_c%'] / 100)
    project_data['2015_pop'] = project_data['2015_c#'] / (project_data['2015_c%'] / 100)

    # User is prompt to input a country. User must input any country from the list of UN Codes.
    while True:
        try:
            chosen_country = input('Please enter a country you would like to analyze: ')
            if  chosen_country not in set(project_data.index.get_level_values('Country')):
                raise ValueError()
            break
        except ValueError:
            print('You must enter a valid country name')

    # Prints out information about the country input by user.        
    country_stats(project_data, chosen_country)
    # Prints out information of the sub-region from the country chosen by the user.
    subreg_stats(project_data, chosen_country)
    
    # A dictionary list of column names is created to help identify the type of information in main merged dataset.
    column_dict = {
    '2005_c%' : 'Number of cellphones per 100 people in 2005',
    '2010_c%' : 'Number of cellphones per 100 people in 2010',
    '2015_c%' : 'Number of cellphones per 100 people in 2015',
    '2005_c#' : 'Total # of cellphones in 2005',
    '2010_c#' : 'Total # of cellphones in 2010',
    '2015_c#' : 'Total # of cellphones in 2015',
    '2005_i%' : '% Internet users in 2005',
    '2010_i%' : '% Internet users in 2010',
    '2015_i%' : '% Internet users in 2015',
    '2005_r' : '% Population annual rate of increase in 2005',
    '2010_r' : '% Population annual rate of increase in 2010',
    '2015_r' : '% Population annual rate of increase in 2015',
    '2005_pop' : 'Total population in  2005',
    '2010_pop' : 'Total population in  2010',
    '2015_pop' : 'Total population in  2015',
    }
    # All columns are renamed according to dictionary list.
    project_data.rename(columns = column_dict, inplace = True)

    # Grouped columns based on year in common and then combined in an array for shorter and easier way to get index.
    array_2005 = np.array(list(column_dict.values())[0:15:3])
    array_2010 = np.array(list(column_dict.values())[1:15:3])
    array_2015 = np.array(list(column_dict.values())[2:15:3])
    column_data = np.array([array_2005, array_2010, array_2015]).reshape((3,5))

    # It prompts user for another input to pull information from columns instead.
    print('\nLet us analyze the basic statistics of a particular set of data for all countries...')
    while True:
        try:
            # User must enter an integer number between 0 - 4 to choose any of the data in the list.
            print('0:   Number of cellphones per 100 people')
            print('1:   Total # of cellphones')
            print('2:   % Internet users')
            print('3:   % Population annual rate of increase')
            print('4:   Total population')
            data_series = input('Please select an index number to choose your data series from the menu above: ')
            if  data_series not in ('0','1','2','3','4'):
                raise ValueError()
            break
        except ValueError:
            print('You must enter a valid number between 0 - 4 from the menu.')

    # User is also prompt to choose a specific year to filter down the year of the chosen data.
    print('\nNow please choose a specific year to pull the information...')
    while True:
        try:
            chosen_year = input('Please select a year between 2005, 2010, or 2015: ')
            if  chosen_year not in ('2005', '2010', '2015'):
                raise ValueError()
            break
        except ValueError:
            print('You must enter a valid year. It has to be either 2005, 2010 or 2015.')
    
    # Based on user's inputs, we find the index number and the column name in our main data.
    if (chosen_year == '2005'):
        print("\nYou have chosen to look into:", column_data[0,int(data_series)])
        chosen_column = column_data[0,int(data_series)]
    elif (chosen_year == '2010'):
        print("\nYou have chosen to look into: ", column_data[1,int(data_series)])
        chosen_column = column_data[1,int(data_series)]
    elif (chosen_year == '2015'):
        print("\nYou have chosen to look into: ", column_data[2,int(data_series)])
        chosen_column = column_data[2,int(data_series)]

    # From the searched column, it prints out the basic stadistics of the subset of data chosen by user.
    print('\n***Stadistics of ', chosen_column, '***')
    print(project_data[chosen_column].dropna().describe())

    # Plots out the trend usage between cellphones and internet for each UN region.
    print('\nNow that we have seen datas about cellphones and internet usage, it would be interesting to know if there is any correlation trend between them.')
    print('We will plot out the trend between regions in cellphone and internet usage...')
    region_cell_int_info(project_data)

    # Last but not least, I added a small analysis to calculate the number of countries that had less than 50% of their population using internet.
    print('\nFUN ANALYSIS:')
    print('How many countries have less than half of their population that uses internet in 2015?')
    internet_data = project_data.loc[:, pd.IndexSlice['% Internet users in 2015']]
    countries_less_internet = internet_data[internet_data < 50].count()
    print('There are ', countries_less_internet, 'countries, that is', int((countries_less_internet / len(project_data.index)) * 100), r'% in the world.')


    # project_data.to_excel(r"./ProjectDataExport.xlsx", index = True, header = True)



if __name__ == '__main__':
    main()

