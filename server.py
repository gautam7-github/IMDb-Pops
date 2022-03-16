import requests
import pandas as pd
import numpy as np
from flask import Flask, jsonify
import json

app = Flask(__name__)
app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True


@app.route("/api/v1/getmovies/popular")
def getData():
    dfs = pd.read_html(
        "https://www.imdb.com/chart/moviemeter/?ref_=nv_mv_mpm")[0]
    dfs.replace(np.nan, "Not Rated", inplace=True)
    top = dfs["Rank & Title"].str.split().str[:-3]
    dfs["Title"] = top.str[:-1].apply(lambda x: ' '.join(map(str, x)))
    dfs["Year"] = top.str[-1]
    dfs.drop(labels=["Unnamed: 0", "Unnamed: 4", "Your Rating",
                     "Rank & Title"], axis=1, inplace=True)
    dfs = dfs.reindex(columns=["Title", "Year", "IMDb Rating"])
    return jsonify(json.loads(dfs.to_json(orient="index")))


app.run(debug=True)
