from flask import Blueprint, render_template, request
from app.services.recommendation import recommend, df

main = Blueprint("main", __name__)

@main.route("/", methods=["GET", "POST"])
def home():

    recommendations = []
    selected_place = ""
    place = None

    if request.method == "POST":

        selected_place = request.form.get("place_name")

        if selected_place:

            hasil = df[
                df["name"].str.lower() == selected_place.lower()
            ]

            if not hasil.empty:
                place = hasil.iloc[0]

            recommendations = recommend(selected_place)

    return render_template(
        "index.html",
        place=place,
        recommendations=recommendations,
        selected_place=selected_place
    )