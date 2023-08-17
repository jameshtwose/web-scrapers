# %%
import pandas as pd
from sqlalchemy import create_engine

# %%
engine = create_engine("sqlite:///hipsy.sqlite")

with engine.connect() as conn:
    df = pd.read_sql("SELECT * FROM hipsy", conn)

# %%
df.head()

# %%
df["page_event_location"].tolist()

# %%
