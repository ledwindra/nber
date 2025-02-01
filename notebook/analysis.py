import json
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import warnings
from glob import glob

# ignore warning
warnings.filterwarnings("ignore")

def bar_plot(df, label, title, column):
    """Returns a bar plot.
    """

    fig, ax = plt.subplots(figsize=(20, 5))
    bar_width = 0.35
    opacity = 0.9
    ax.bar(df.index,
        height="count",
        width=0.5,
        data=df,
        alpha=opacity,
        color="black",
        label=label)
    plt.title(title)
    plt.ylabel("Total papers")
    plt.xticks(df.index, df[column])
    plt.yticks()
    vals = ax.get_yticks()
    ax.grid(True, axis="y", linewidth=1, alpha=0.25)
    plt.show()
    
def citation(df):
    """Returns a scatter plot of citations.
    """

    df = df[["cites", "cited_by"]]
    # log scale
    df["log_total_cites"] = df.apply(lambda x: np.log(x["cites"]), axis=1)
    df["log_cited_by"] = df.apply(lambda x: np.log(x["cited_by"]), axis=1)
    
    fig, ax = plt.subplots(figsize=(20, 5))
    plt.scatter(x="log_total_cites", y="log_cited_by", data=df, c="black")
    plt.title("Citations in NBER (no causality implied)")
    plt.xlabel("Total cites per paper")
    plt.ylabel("Total cited per paper")
    plt.show
    
def citation_density(df):
    """Returns a density plot of citations.
    """

    # log scale
    df["log_total_cites"] = df.apply(lambda x: np.log(x["cites"]), axis=1)
    df["log_cited_by"] = df.apply(lambda x: np.log(x["cited_by"]), axis=1)

    # visualize
    fig, ax = plt.subplots(figsize=(20, 5))
    # must be > 0 otherwise error appears
    sns.kdeplot(df[df["log_total_cites"] > 0]["log_total_cites"], shade=True, color="red")
    sns.kdeplot(df[df["log_cited_by"] > 0]["log_cited_by"], shade=True, color="blue")

    # show median values
    log_total_cites_median = np.median(df["log_total_cites"][~np.isnan(df["log_total_cites"])])
    log_cited_by_median = np.median(df["log_cited_by"][~np.isnan(df["log_cited_by"])])
    
    ax.axvline(log_total_cites_median, color="red")
    ax.axvline(log_cited_by_median, color="blue")

    caption = f"Vertical lines show median citations:\n-Total cites: {round(log_total_cites_median, 2)}\n-Total cited by: {round(log_cited_by_median, 2)}"
    fig.text(0.1, -0.05, caption)
    plt.title("Distributions of citations in NBER in log scale")
    plt.xlabel("Citations")
    plt.show()
    
def collaboration(df, y_interval, y_max):
    """Returns a line plot of mean total authors over periods of time.
    """

    # transform data
    df = df[df["citation_publication_date"].isna() == False]
    df = df[["citation_publication_date", "citation_author"]]
    df["total_author"] = df.apply(lambda x: len(x["citation_author"]), axis=1)
    df["year"] = df.apply(lambda x: x["citation_publication_date"][:4], axis=1)
    df = df[df["year"] != "None"]
    df["year"] = df["year"].astype(int)
    df = df.groupby("year")["total_author"].agg("mean")
    df = df.to_frame().reset_index()
    df = df.rename(columns={"total_author": "mean_total_author"})
    
    # visualize data
    fig, ax = plt.subplots(figsize=(20, 5))
    plt.plot("year", "mean_total_author", data=df, color="black")
    plt.title(f"Mean total authors per paper by year")
    plt.xlabel("Year")
    plt.ylabel("Mean total authors")
    plt.xticks(np.arange(df.year.min(), df.year.max()+1, 1), rotation=45)
    plt.yticks(np.arange(0, max(df["mean_total_author"])+y_max, y_interval))
    ax.grid(True, linewidth=1, alpha=0.25)
    plt.show
    
def count_by_year(df):
    """Returns a count of papers by year.
    """

    df = df[df["citation_publication_date"].isna() == False]
    count = df[["id", "citation_publication_date"]]
    count["citation_publication_date"] = count.apply(lambda x: x["citation_publication_date"][:4], axis=1)
    count = count.groupby("citation_publication_date").size().to_frame().reset_index()
    count = count.rename(columns={0: "count", "citation_publication_date": "year"})
    
    return count
    
def get_data(file_name):
    """Returns a DataFrame from a JSON file.
    """

    df = glob(f"../data/{file_name}/*")
    df = [json.load(open(x, "r")) for x in df]
    df = pd.DataFrame(df)
    if file_name == "nber":
        df["year"] = df["citation_publication_date"].str[:4].astype(int)
        df = df[df.year <= 2024]
    
    return df

def distribution(df):
    df = df.explode("citation_author")[["citation_author"]]
    df = df.groupby("citation_author").size().to_frame().reset_index()
    df.rename(columns={0: "count"}, inplace=True)
    sns.histplot(data=df, x="count", bins=50, color="gray", stat="density")
    plt.title("Distributions of published papers by authors")
    plt.show

def published_paper(df, title, x_interval, y_interval, y_max):
    """Returns a line plot of published papers over periods of time.
    """

    df = df[df["year"] != "None"]
    df["year"] = df["year"].astype(int)
    fig, ax = plt.subplots(figsize=(20, 5))
    plt.plot("year", "count", data=df, color="black")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Total papers")
    plt.xticks(np.arange(df.year.min(), df.year.max()+1, x_interval), rotation=45)
    plt.yticks(np.arange(0, max(df["count"])+y_max, y_interval))
    ax.grid(True, linewidth=1, alpha=0.25)
    plt.show()
    
def section_trends(df, column, title, keyword, x_interval, y_interval, y_max):
    """Plot a line plot of trends in the field of economics over periods of time.
    """

    # transform data
    df = df[["citation_publication_date", column]]
    df[column] = df[column].fillna("N/A")
    df.loc[:, "year"] = df.apply(lambda x: x["citation_publication_date"][:4], axis=1)
    df = df[df["year"] != "None"]
    df["year"] = df["year"].astype(int)
    df.loc[:, column] = df.apply(lambda x: x[column].lower(), axis=1)
    df = df[df.apply(lambda x: keyword in x[column], axis=1) == True]
    df = df.groupby("year").size().to_frame().reset_index()
    df = df.rename(columns={0: "count"})

    # visualize time series
    fig, ax = plt.subplots(figsize=(20, 5))
    plt.plot("year", "count", data=df, color="black")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Total papers")
    plt.xticks(np.arange(df.year.min(), df.year.max()+1, x_interval), rotation=45)
    plt.yticks(np.arange(0, max(df["count"])+y_max, y_interval))
    ax.grid(True, linewidth=1, alpha=0.25)
    plt.show()
    
def top_five(df, column="topics"):
    """Returns a DataFrame of the top five most common topics.
    """

    df = df[df[column].isna() == False]
    df = df[[column]]
    df = df.explode(column)
    df = df.groupby(column).size().to_frame().reset_index()
    df = df.rename(columns={0: "count"})
    df = df.sort_values(by="count", ascending=False)
    df = df[~df[column].isin(["", ", ", "\n"])]
    df = df.reset_index(drop=True)
    df = df.iloc[:5, :]
    df.index = range(1,6)
    
    return df

def top_five_trends(df, column, title, y_interval):
    """Returns a line plot of the top five most common topics over periods of time.
    """

    # transform
    df = df[["citation_publication_date", column]]
    df = df.explode(column)
    df["year"] = df.apply(lambda x: x["citation_publication_date"][:4], axis=1)
    df = df[df["year"] != "None"]
    df["year"] = df["year"].astype(int)
    df = df[["year", column]]
    df = df[~df[column].isin(["", ", ", "\n"])]
    top_five = df.groupby(column).size().to_frame().reset_index().sort_values(by=0, ascending=False)
    top_five = top_five.reset_index(drop=True)[:5][column].to_list()
    df = df[df[column].isin(top_five)]
    dfs = [df[df[column] == x].groupby("year").size() for x in top_five]
    dfs = [x.to_frame().reset_index().rename(columns={0: "count"}) for x in dfs]
    ymin = min([x["count"].max() for x in dfs])
    ymax = max([x["count"].max() for x in dfs])
    
    # visualize
    fig, ax = plt.subplots(figsize=(20, 5))
    plt.plot("year", "count", data=dfs[0], color="black")
    plt.plot("year", "count", "--", data=dfs[1], color="red")
    plt.plot("year", "count", data=dfs[2], color="blue")
    plt.plot("year", "count", "--", data=dfs[3], color="green")
    plt.plot("year", "count", data=dfs[4], color="orange")
    plt.title(title)
    plt.xlabel("Year")
    plt.ylabel("Total papers")
    plt.xticks(np.arange(df.year.min(), df.year.max()+1, 1), rotation=45)
    plt.yticks(np.arange(0, ymax+1, y_interval))
    ax.legend(labels=top_five, loc="best")
    ax.grid(True, linewidth=1, alpha=0.25)
    plt.show()
