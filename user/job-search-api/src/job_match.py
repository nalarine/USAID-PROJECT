from json import dumps, loads

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics import DistanceMetric

from src.constants import globals as g

model = SentenceTransformer(g.MODEL)
job_lists = g.JOB_LISTINGS


def text_embedding(text: str) -> np.array:
    """Converts text to embeddings.

    Parameters
    ----------
    text : str
        Text in string format.

    Returns
    -------
    np.array
        Returns the encoded embeddings with 728 features.
    """
    return model.encode(text)


def user_query(query: str | list[str], k: int) -> np.array:
    """Generate top-k job results based on user query.

    Parameters
    ----------
    query : list
        List of keywords/skill.
    k : int
        Number of jobs to return.

    Returns
    -------
    np.array
        Returns the indices of the top-k results.
    """
    
    # if query is list, convert to string
    # if str(type(query)) == "<class 'list'>":
    if type(query) is list:
        embedded_query = text_embedding(", ".join(query))
        print("Converting list to string ...")
    else:
        embedded_query = text_embedding(query)

    dist = DistanceMetric.get_metric("euclidean")

    distances = dist.pairwise(
        g.EMBEDDINGS,
        embedded_query.reshape(1, -1),
    ).flatten()

    results = np.argsort(distances)
    top_k_jobs = job_lists.iloc[results[:k]].to_json(orient="records")

    return top_k_jobs


if __name__ == "__main__":
    params = {
        "query": "public speaking, communication",
        "k": 5,
    }

    print(user_query(**params))
