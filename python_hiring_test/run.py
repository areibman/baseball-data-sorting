"""Main script for generating output.csv."""
import pandas as pd
import os

def main():
    # add basic program logic here
    #Read in ./data/raw/pitchdata.csv
    dirname = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(os.path.join(dirname, 'data','raw','pitchdata.csv'))
    combinations = pd.read_csv(os.path.join(dirname, 'data','reference','combinations.txt'))

    MAXIMUM_PA = 25

    def createStatistics(dataframe):
        """
        Adds AVG, OBP, SLG, and OPS columns to dataframe and rounds to 3 digits
        """
        # AVG- hits divided by at bats (H/AB)
        dataframe['AVG'] = dataframe['H']/dataframe['AB']

        # OBP- times reached base (H + BB + HBP)/(AB + BB + HBP + SF).
        dataframe['OBP'] = (dataframe['H']+dataframe['BB']+dataframe['HBP'])/ \
        (dataframe['AB']+dataframe['BB']+dataframe['HBP']+dataframe['SF'])

        # SLG- total bases achieved on hits divided by at-bats (TB/AB)
        dataframe['SLG'] = dataframe['TB']/dataframe['AB']

        # OPS- on-base percentage plus slugging average
        dataframe['OPS'] = dataframe['OBP'] + (dataframe['TB']/dataframe['AB'])
        
        #Round statistics
        dataframe[['AVG','OBP','SLG','OPS']] = dataframe[['AVG','OBP','SLG','OPS']].apply(lambda x: x.round(3))

    output_list = []

    for comb in combinations.iloc[:].as_matrix():
        #For each row in combinations, identify the groupings
        stat, subject, split = comb

        #Determine which side of the field the player is facing against
        if split == 'vs RHP': versus, side = 'PitcherSide', 'R'
        if split == 'vs LHP': versus, side = 'PitcherSide', 'L'
        if split == 'vs RHH': versus, side = 'HitterSide', 'R'
        if split == 'vs LHH': versus, side = 'HitterSide', 'L'

        grouped = df.groupby([subject,versus],as_index=False).sum()
        #Remove all items that are less than the PA threshold
        grouped = grouped[(grouped[versus]==side) & (grouped['PA'] >= MAXIMUM_PA)]
        #Create statistics for the dataframe
        createStatistics(grouped)
        
        #Reorganize and columns to perfectly match output
        grouped['Split'] = split
        grouped['Subject'] = grouped.columns[0]
        grouped['Stat'] = stat
        grouped['Value'] = grouped[stat] 
        grouped = grouped.rename(index = str, columns = {subject: 'SubjectId'})
        output_list.append(grouped[['SubjectId','Value','Split', 'Subject','Stat']])

    #Sort values and columns correctly
    statistics_df = pd.concat(output_list)
    statistics_df = statistics_df.reindex(columns= 
                                        ['SubjectId','Stat','Split','Subject','Value'])
    statistics_df.sort_values(by = 
                            ['SubjectId','Stat','Split','Subject','Value'], inplace = True)
    statistics_df.set_index('SubjectId', inplace=True)
    
    statistics_df.to_csv(os.path.join(dirname, 'data','processed','output.csv'))


if __name__ == '__main__':
    main()
