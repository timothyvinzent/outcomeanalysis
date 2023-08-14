import pandas as pd
from collections import defaultdict

def outcome_distribution_builder(df_outcome, outcomes_labels, lst_of_predicates):
    filtered_dataframes = []
    overlap_check = []
    values = []

    for i in range(len(outcomes_labels)):
        df_outcome[outcomes_labels[i]] = df_outcome.apply(lst_of_predicates[i], axis=1)
        filtered_dataframes.append(df_outcome.loc[df_outcome[outcomes_labels[i]] == True, ['case_id']])
        values.append([len(filtered_dataframes[i])])

    for l in range(len(filtered_dataframes)):
        if l == 0:
            unresolved = df_outcome.loc[~df_outcome['case_id'].isin(filtered_dataframes[l]['case_id']), ['case_id']]
        else:
            unresolved = unresolved.loc[~unresolved['case_id'].isin(filtered_dataframes[l]['case_id']), ['case_id']]

    dct = defaultdict(list)

    # Loop over the list and append the combinations to the dictionary
    for i in range(len(outcomes_labels)):
        for j in range(i+1, len(outcomes_labels)):
            dct[outcomes_labels[i]].append(outcomes_labels[j])
            overlap_check.append(len(pd.merge(filtered_dataframes[i], filtered_dataframes[j], how='inner', on=['case_id'])))
    # Convert the defaultdict to a regular dict
    dct = dict(dct)
    k = 0 # index for values
    for key, value in dct.items():
        
        for i in range(len(value)):
            
            value[i] = (value[i], overlap_check[k]) # make a tuple of string and value
            k += 1 # increment index
    print(dct)
    values.append([len(unresolved)])

    return values, dct