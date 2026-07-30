import pandas as pd

def recommend(place_name, top_n=5):

    print("\n===================================")
    print("Pencarian :", place_name)

    hasil = df[
        df["name"].str.lower().str.contains(
            place_name.lower(),
            na=False
        )
    ]

    print("Jumlah hasil pencarian :", len(hasil))

    if hasil.empty:
        print("Destinasi tidak ditemukan.")
        return []

    idx = hasil.index[0]

    print("Index ditemukan :", idx)
    print("Nama :", df.iloc[idx]["name"])

    # Hitung similarity
    sim_scores = list(enumerate(cosine_sim[idx]))

    sim_scores = sorted(
        sim_scores,
        key=lambda x: x[1],
        reverse=True
    )

    # Ambil top_n termasuk dirinya sendiri
    sim_scores = sim_scores[:top_n]

    rekomendasi = []

    for i, score in sim_scores:

        rating = df.iloc[i]["rating"]

        # Jika rating kosong, NaN, atau tulisan "nan"
        if (
            pd.isna(rating)
            or str(rating).strip().lower() == "nan"
            or str(rating).strip() == ""
        ):
            rating = "-"

        rekomendasi.append({
            "name": df.iloc[i]["name"],
            "type": df.iloc[i]["type"],
            "rating": rating,
            "address": df.iloc[i]["address"],
            "latitude": df.iloc[i]["latitude"],
            "longitude": df.iloc[i]["longitude"],
            "image": df.iloc[i]["image"],
            "similarity": round(float(score), 4),
            "selected": (i == idx)
        })

    print("Rekomendasi:")
    for item in rekomendasi:
        print("-", item["name"], item["similarity"])

    return rekomendasi