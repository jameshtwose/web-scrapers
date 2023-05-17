# %%
import os
from dotenv import load_dotenv, find_dotenv
from pyspark.context import SparkContext
from pyspark.sql import SQLContext
# %%
_ = load_dotenv(find_dotenv())
# %%
sc = SparkContext(master="local", appName="ds")
# %%
sqlContext = SQLContext(sc)

# %%
url = os.getenv("SPORTS_SCRAPER_POSTGRES_URL")
# %%
df = sqlContext.read.format("jdbc").options(
    url=url,
    driver="org.postgresql.Driver",
    dbtable="opta_power_data").load()


# %%
# sqlContext.sql("CREATE DATABASE IF NOT EXISTS ds")
sc.stop()
# %%
