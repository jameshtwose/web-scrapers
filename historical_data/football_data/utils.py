def convert_numeric(col):
    try:
        return col.astype(float)
    except (TypeError, ValueError):
        return col

# label wins/losses/draws with respect to team of interest
def label_wins_losses_draws(row, team_of_interest):
    """Label wins/losses/draws with respect to team of interest. Intended to be used with pd.DataFrame.apply.
    
    Parameters
    ==========
    row: pd.Series
        row of a dataframe
    team_of_interest: str
        team of interest
    
    Returns
    =======
    pd.Series
    
    Examples
    ========
    >>> df.apply(lambda x: label_wins_losses_draws(x, "Portsmouth"), axis=1)
    
    """
    if row["FTR"] == "H" and row["HomeTeam"] == team_of_interest:
        return "win"
    elif row["FTR"] == "A" and row["AwayTeam"] == team_of_interest:
        return "win"
    elif row["FTR"] == "D":
        return "draw"
    else:
        return "loss"