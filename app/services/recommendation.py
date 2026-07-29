import pickle
from pathlib import Path

# ==========================
# Load Model
# ==========================

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models"

with open(MODEL_DIR / "dataset.pkl", "rb") as f:
    df = pickle.load(f)

with open(MODEL_DIR / "tfidf.pkl", "rb") as f:
    tfidf = pickle.load(f)

with open(MODEL_DIR / "cosine_similarity.pkl", "rb") as f:
    cosine_sim = pickle.load(f)

print("Model AI berhasil dimuat.")
print("Jumlah data :", len(df))
print("Kolom :", df.columns.tolist())


# ==========================
# Fungsi Rekomendasi
# ==========================

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

    # Ambil 5 hasil termasuk dirinya sendiri
    sim_scores = sim_scores[:top_n]

    rekomendasi = []

    for i, score in sim_scores:

        rekomendasi.append({
            "name": df.iloc[i]["name"],
            "type": df.iloc[i]["type"],
            "rating": df.iloc[i]["rating"],
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