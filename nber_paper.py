import matplotlib.font_manager as font_manager
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import re
import requests
import seaborn as sns
import statistics
import warnings

# set xkcd mode for plotting
font_manager._rebuild()
plt.xkcd()

# ignore warning
warnings.filterwarnings('ignore')

def bar_plot(df, label, title, column, x_caption=0, y_caption=0):
    fig, ax = plt.subplots(figsize=(15, 5))
    bar_width = 0.35
    opacity = 0.9
    ax.bar(
        df.index,
        height='count',
        width=0.5,
        data=df,
        alpha=opacity,
        color='black',
        label=label
    )
    plt.title(title)
    plt.ylabel('Jumlah paper')
    plt.xticks(df.index)
    plt.yticks()
    
    caption_a = lambda df, column: ' \n'.join([f'{df.index[x]}: {df[column][x]}' for x in range(len(df))])
    plt.text(x_caption, y_caption, caption_a(df, column))
    vals = ax.get_yticks()
    ax.legend()
    plt.show()
    
def citation(df):
    df = df[['total_cites', 'cited_by']]
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.scatter(x='total_cites', y='cited_by', data=df, c='black')
    plt.title('Citations in NBER (no causality implied)')
    plt.xlabel('Total cites per paper')
    plt.ylabel('Total cited per paper')
    plt.show
    
def citation_density(df):
    # log scale
    df['log_total_cites'] = df.apply(lambda x: np.log(x['total_cites']), axis=1)
    df['log_cited_by'] = df.apply(lambda x: np.log(x['cited_by']), axis=1)
    
    # visualize
    fig, ax = plt.subplots(figsize=(15, 5))
    # must be > 0 otherwise error appears
    sns.kdeplot(df[df['log_total_cites'] > 0]['log_total_cites'], shade=True, color='red')
    sns.kdeplot(df[df['log_cited_by'] > 0]['log_cited_by'], shade=True, color='blue')

    # show median values
    ax.axvline(statistics.median(df['log_total_cites']), color='red')
    ax.axvline(statistics.median(df['log_cited_by']), color='blue')
    
    # exponentiate median values
    total_cites = int(np.exp(statistics.median(df['log_total_cites'])))
    cited_by = int(np.exp(statistics.median(df['log_cited_by'])))

    caption = f"Vertical lines show median citations: \n \tTotal cites: {total_cites} \n \tTotal cited by: {cited_by}"
    plt.title('Distributions of citations in NBER (log scale)')
    fig.text(0.1, -0.05, caption)
    
def collaboration(df):
    # transform data
    df = df[df['citation_date'].isna() == False]
    df = df[['citation_date', 'citation_author']]
    df['citation_author'] = df.apply(lambda x: re.sub('[^A-Za-z0-9,\' ]+', '', x['citation_author']), axis=1)
    df['citation_author'] = df.apply(lambda x: x['citation_author'].split('\''), axis=1)
    df['citation_author'] = df.apply(lambda x: [x for x in x['citation_author'] if x != '' and x != ', '], axis=1)
    df['total_author'] = df.apply(lambda x: len(x['citation_author']), axis=1)
    df['year'] = df.apply(lambda x: int(x['citation_date'][:4]), axis=1)
    df = df.groupby('year')['total_author'].agg('median')
    df = df.to_frame().reset_index()
    df = df.rename(columns={'total_author': 'median_total_author'})
    
    # visualize data
    min_year = min(df['year'])
    min_year = int(str(min_year).replace(str(min_year)[-1], '0'))
    max_year = max(df['year'])
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.plot('year', 'median_total_author', data=df, color='black')
    plt.title(f'Median total authors per paper each year')
    plt.xlabel('Year')
    plt.ylabel('Median total author')
    plt.xticks(np.arange(min_year, max_year+1, 3))
    plt.yticks(np.arange(min(df['median_total_author']), max(df['median_total_author'])+1, 1))
    plt.show
    
def count_by_year(df):
    df = df[df['citation_date'].isna() == False]
    count = df[['id', 'citation_date']]
    count['citation_date'] = count.apply(lambda x: int(x['citation_date'][:4]), axis=1)
    count = count.groupby('citation_date').size().to_frame().reset_index()
    count = count.rename(columns={0: 'count', 'citation_date': 'year'})
    
    return count
    
def get_data(file_name):
    df = pd.read_csv(file_name, sep='|')
    df = df[~df['id'].isna() == True]
    df['id'] = df['id'].astype(int)
    
    return df

def published_paper(df, title, x_interval=1, y_interval=1):
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.plot('year', 'count', data=df, color='black')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Total paper')
    min_year = min(df['year'])
    min_year = int(str(min_year).replace(str(min_year)[-1], '0'))
    plt.xticks(np.arange(min_year, max(df['year'])+1, x_interval))
    plt.yticks(np.arange(0, max(df['count'])+1, y_interval))
    plt.show
    
def section_trends(df, column, title, keyword, x_interval, y_interval):
    # transform data
    df = df[df['citation_date'].isna() == False]
    df = df[['citation_date', column]]
    df[column] = df[column].fillna('N/A')
    df.loc[:, 'year'] = df.apply(lambda x: int(x['citation_date'][:4]), axis=1)
    min_year = min(df['year'])
    min_year = int(str(min_year).replace(str(min_year)[-1], '0'))
    max_year = max(df['year'])
    df.loc[:, column] = df.apply(lambda x: x[column].lower(), axis=1)
    df = df[df.apply(lambda x: keyword in x[column], axis=1) == True]
    df = df.groupby('year').size().to_frame().reset_index()
    df = df.rename(columns={0: 'count'})

    # visualize tiem series
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.plot('year', 'count', data=df, color='black')
    plt.title(f'NBER trends: {title} in the {column} section in NBER')
    plt.xlabel('Year')
    plt.ylabel('Total paper')
    plt.xticks(np.arange(min_year, max_year+1, x_interval))
    plt.yticks(np.arange(0, max(df['count'])+1, y_interval))
    plt.show
    
def top_five(df, column='topics', split_by=','):
    df = df[df[column].isna() == False]
    df = df[[column]]
    if column == 'citation_author':
        df.loc[:, column] = df.apply(lambda x: re.sub('[^A-Za-z0-9,\' ]+', '', x[column]), axis=1)
    else:
        df.loc[:, column] = df.apply(lambda x: re.sub('[^A-Za-z0-9 ]+', '', x[column]), axis=1)
    df.loc[:, column] = df.apply(lambda x: x[column].split(split_by), axis=1)
    df = df.explode(column)
    df = df.groupby(column).size().to_frame().reset_index()
    df = df.rename(columns={0: 'count'})
    df = df.sort_values(by='count', ascending=False)
    df = df[~df[column].isin(['', ', '])]
    df = df.reset_index(drop=True)
    df = df.iloc[:5, :]
    
    return df

def top_five_trends(df, column, split_by, title):
    # transform
    df = df[df[column].isna() == False]
    in_array = lambda value, column: df[df.apply(lambda x: value in x[column], axis=1) == True]
    df_top_five = top_five(df, column, split_by)[column]
    df0 = count_by_year(in_array(df_top_five[0], column))
    df1 = count_by_year(in_array(df_top_five[1], column))
    df2 = count_by_year(in_array(df_top_five[2], column))
    df3 = count_by_year(in_array(df_top_five[3], column))
    df4 = count_by_year(in_array(df_top_five[4], column))
    
    # visualize
    fig, ax = plt.subplots(figsize=(15, 5))
    plt.plot('year', 'count', data=df0, color='black')
    plt.plot('year', 'count', '--', data=df1, color='red')
    plt.plot('year', 'count', data=df2, color='blue')
    plt.plot('year', 'count', '--', data=df3, color='green')
    plt.plot('year', 'count', data=df4, color='orange')
    plt.title(title)
    plt.xlabel('Year')
    plt.ylabel('Total paper')
    ax.legend(labels=[df_top_five[0], df_top_five[1], df_top_five[2], df_top_five[3], df_top_five[4]])
    plt.show()
