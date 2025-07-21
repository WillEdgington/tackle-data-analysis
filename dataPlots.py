import pandas as pd
import matplotlib.pyplot as plt

def filterAttemptNumberFromType(df: pd.DataFrame) -> pd.DataFrame:
    """Removes the attempt number out of tackle type
    """
    df['Type'] = df['Type'].str.replace(r'\d+$', '', regex=True)
    return df

def filterForPart(part: str, df: pd.DataFrame) -> pd.DataFrame:
    """Filters results DataFrame for specific body part.

    Args:
        part (string): the body part to filter for
        df (DataFrame): the results DataFrame
    Returns:
        filteredDf (DataFrame): the results dataframe filtered for specified body part
    """
    filteredDf = df[df['Part']==part]
    return filteredDf

def filterForType(type: set[str], df: pd.DataFrame) -> pd.DataFrame:
    """Filters results DataFrame for specific type of tackle.

    Args:
        type (set[string]): the type of tackles to filter for
        df (DataFrame): the results DataFrame
    Returns:
        filteredDf (DataFrame): the results dataframe filtered for specified tackle type part
    """
    filteredDf = df[df['Type'].isin(type)]
    return filteredDf

def filterForSubject(subject: str, df: pd.DataFrame) -> pd.DataFrame:
    """Filters results DataFrame for specific test subject.

    Args:
        type (string): the test subject to filter for
        df (DataFrame): the results DataFrame
    Returns:
        filteredDf (DataFrame): the results dataframe filtered for specified tackle type part
    """
    filteredDf = df[df['Subject']==subject]
    return filteredDf

def create3DPlot(df: pd.DataFrame, groupKey: str="Type", title: str="Analysis"):
    """Creates 3D scatter plot of results

    Args:
        df (DataFrame): the results DataFrame
        groupKey (string): the key for which column of results decides the colour of the points
        title (string): title of the scatter plot
    """
    groups = df[groupKey].unique()
    groupToColour = {g: c for g, c in zip(groups, plt.cm.tab20.colors)}

    colours = df[groupKey].map(groupToColour)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot(projection='3d')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    sc = ax.scatter(df['X'], df['Y'], df['Z'], c=colours)

    for g in groups:
        ax.scatter([], [], [], color=groupToColour[g], label=g)
    ax.legend(title=groupKey)

    plt.title(title)
    plt.show()

def createXYPlot(df: pd.DataFrame, groupKey: str="Type", title: str="Analysis"):
    """Creates 2D scatter plot of X and Y values in results

    Args:
        df (DataFrame): the results DataFrame
        groupKey (string): the key for which column of results decides the colour of the points
        title (string): title of the scatter plot
    """
    groups = df[groupKey].unique()
    groupToColour = {g: c for g, c in zip(groups, plt.cm.tab20.colors)}

    colours = df[groupKey].map(groupToColour)

    fig = plt.figure(figsize=(12, 12))
    ax = fig.add_subplot()

    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    sc = ax.scatter(df['X'], df['Y'], c=colours)

    for g in groups:
        ax.scatter([], [], [], color=groupToColour[g], label=g)
    ax.legend(title=groupKey)

    plt.title(title)
    plt.show()

df = pd.read_csv('data/CleanedResults.csv')
df = filterAttemptNumberFromType(df)

for part in df['Part'].unique():
    filteredDf = filterForPart(part=part, df=df)
    filteredDf = filterForType(type={"R","L"}, df=filteredDf)
    # filteredDf = filterForSubject(subject="S1", df=filteredDf)

    create3DPlot(filteredDf, groupKey='Type',title=part)
    createXYPlot(filteredDf, groupKey='Type',title=part)
