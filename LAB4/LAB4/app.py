from flask import Flask, render_template, request

app = Flask(__name__)

# =========================
# PERSONAL INFORMATION
# Replace these sample values with your own data.
# =========================
PROFILE = {
    "name": "Elaine Zaire S. Gonzales",
    "course": "BS Computer Engineering",
    "section": "2-3",
    "school": "Polytechnic University of the Philippines",
    "email": "gonzaleselainezaire@gmail.com",
    "location": "Antipolo City, Rizal Province, Philippines",
    "motto": "Float like a butterfly and sting like a bee",
    "about": "Enjoy your life to the fullest.",
    "skills": ["Python", "CSS"],
}

# =========================
# LINK LIST
# Replace these with your own links.
# =========================
LINKS = [
    {
        "name": "GitHub",
        "url": "https://github.com/Elaine04-dsa",
        "description": "My coding projects and repositories."
    },
    {
        "name": "Facebook",
        "url": "https://www.facebook.com/eleeynnnzaire/about",
        "description": "My social profile."
    },
    {
        "name": "Instagram",
        "url": "https://www.instagram.com/eleeyynnn_/",
        "description": "My social profile."
    },
]


@app.route("/")
def index():
    return render_template("index.html", profile=PROFILE)


@app.route("/profile")
def profile():
    return render_template("profile.html", profile=PROFILE)


@app.route("/works", methods=["GET", "POST"])
def works():
    result = None

    if request.method == "POST":
        input_string = request.form.get("inputString", "")
        result = input_string.upper()

    return render_template("touppercase.html", result=result, profile=PROFILE)


# =========================
# AREA OF CIRCLE
# =========================
@app.route("/works/area/circle", methods=["GET", "POST"])
def acircle():
    result = None
    error = None

    if request.method == "POST":
        try:
            radius = float(request.form.get("radius", ""))
            if radius < 0:
                raise ValueError
            result = 3.141592653589793 * radius * radius
        except ValueError:
            error = "Please enter a valid non-negative number."

    return render_template(
        "circle.html",
        result=result,
        error=error,
        profile=PROFILE
    )


# =========================
# AREA OF TRIANGLE
# =========================
@app.route("/works/area/triangle", methods=["GET", "POST"])
def atriangle():
    result = None
    error = None

    if request.method == "POST":
        try:
            base = float(request.form.get("base", ""))
            height = float(request.form.get("height", ""))

            if base < 0 or height < 0:
                raise ValueError

            result = 0.5 * base * height
        except ValueError:
            error = "Please enter valid non-negative numbers."

    return render_template(
        "triangle.html",
        result=result,
        error=error,
        profile=PROFILE
    )


# =========================
# CONTACT
# =========================
@app.route("/contact", methods=["GET", "POST"])
def contact():
    submitted = False

    if request.method == "POST":
        submitted = True

    return render_template(
        "contact.html",
        profile=PROFILE,
        submitted=submitted
    )


# =========================
# LINK LIST
# =========================
@app.route("/links")
def links():
    return render_template(
        "links.html",
        profile=PROFILE,
        links=LINKS
    )


if __name__ == "__main__":
    app.run(debug=True)
