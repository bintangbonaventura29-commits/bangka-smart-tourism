import pickle
import pandas as pd
from rapidfuzz import process, fuzz

with open("app/models/master.pkl","rb") as f:
    df = pickle.load(f)

with open("app/models/tfidf.pkl","rb") as f:
    tfidf = pickle.load(f)

with open("app/models/cosine_sim.pkl","rb") as f:
    similarity = pickle.load(f)

df["name"] = df["name"].astype(str)
df["content"] = df["content"].astype(str)

def recommend(query, top_n=5):

    if not query:
        return []

    keyword = query.lower().strip()

    # =====================================================
    # 1. Exact Match
    # =====================================================

    exact = df[
        df["name"].str.lower() == keyword
    ]

    if not exact.empty:

        idx = exact.index[0]

        sim_scores = list(enumerate(similarity[idx]))

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:top_n+1]

        hasil = []

        for i, score in sim_scores:

            row = df.iloc[i]

            hasil.append({

                "name": row["name"],
                "type": row["type"],
                "rating": row["rating"] if pd.notna(row["rating"]) else "-",
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "image": row["image"],
                "similarity": round(score * 100, 2),
                "selected": False

            })

        return hasil

    # =====================================================
    # 2. Cari keyword pada NAME
    # Contoh:
    # pantai
    # bukit
    # museum
    # air terjun
    # =====================================================

    hasil = (
    df[
        df["name"].str.lower().str.contains(keyword, na=False)
    ]
    .sort_values(
        by="rating",
        ascending=False,
        na_position="last"
    )
    .head(top_n)
)

    if not hasil.empty:

        data = []

        for _, row in hasil.iterrows():

            data.append({

                "name": row["name"],
                "type": row["type"],
                "rating": row["rating"] if pd.notna(row["rating"]) else "-",
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "image": row["image"],
                "similarity": 0,
                "selected": False

            })

        return data

    # =====================================================
    # 3. Cari keyword pada CONTENT
    # =====================================================

    hasil = (
    df[
        df["content"].str.lower().str.contains(keyword, na=False)
    ]
    .sort_values(
        by="rating",
        ascending=False,
        na_position="last"
    )
    .head(top_n)
)
    if not hasil.empty:

        data = []

        for _, row in hasil.iterrows():

            data.append({

                "name": row["name"],
                "type": row["type"],
                "rating": row["rating"] if pd.notna(row["rating"]) else "-",
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "image": row["image"],
                "similarity": 0,
                "selected": False

            })

        return data

    # =====================================================
    # 4. RapidFuzz
    # =====================================================

    match = process.extractOne(
        keyword,
        df["name"].str.lower(),
        scorer=fuzz.WRatio
    )

    if match:

        idx = df[
            df["name"].str.lower() == match[0]
        ].index[0]

        sim_scores = list(enumerate(similarity[idx]))

        sim_scores = sorted(
            sim_scores,
            key=lambda x: x[1],
            reverse=True
        )[1:top_n+1]

        hasil = []

        for i, score in sim_scores:

            row = df.iloc[i]

            hasil.append({

                "name": row["name"],
                "type": row["type"],
                "rating": row["rating"] if pd.notna(row["rating"]) else "-",
                "address": row["address"],
                "latitude": row["latitude"],
                "longitude": row["longitude"],
                "image": row["image"],
                "similarity": round(score * 100, 2),
                "selected": False

            })

        return hasil

    return []