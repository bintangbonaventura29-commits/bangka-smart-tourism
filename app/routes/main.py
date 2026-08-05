from flask import Blueprint, render_template, request
from app.services.recommendation import recommend, df

main = Blueprint("main", __name__)


@main.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    selected_place = ""
    place = None

    if request.method == "POST":

        selected_place = request.form.get("place_name", "").strip()

        if selected_place:

            keyword = selected_place.lower()

            # ======================================
            # 1. Exact Match
            # ======================================
            hasil = df[
                df["name"].str.lower() == keyword
            ]

            # ======================================
            # 2. Partial Match Nama
            # ======================================
            if hasil.empty:

                hasil = df[
                    df["name"].str.lower().str.contains(keyword, na=False)
                ]

            # ======================================
            # 3. Match Berdasarkan Kategori (Type)
            # ======================================
            if hasil.empty:

                hasil = df[
                    df["type"].str.lower().str.contains(keyword, na=False)
                ]

            # ======================================
            # Jika ditemukan
            # ======================================
            if not hasil.empty:

                place = hasil.iloc[0]

                # gunakan nama destinasi hasil pencarian
                recommendations = recommend(selected_place)

            else:

                # fallback ke fuzzy search di recommendation.py
                recommendations = recommend(selected_place)

    return render_template(
        "index.html",
        place=place,
        recommendations=recommendations,
        selected_place=selected_place
    )