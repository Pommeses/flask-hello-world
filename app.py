import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Hilfsfunktion: Blogposts laden
def load_posts():
    with open("package.json", "r") as file:
        return json.load(file)

# Hilfsfunktion: Blogposts speichern
def save_posts(posts):
    with open("package.json", "w") as file:
        json.dump(posts, file, indent=4)

@app.route('/')
def index():
    posts = load_posts()
    return render_template("index.html", posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        posts = load_posts()

        # Neue ID: max. vorhandene ID + 1
        new_id = max([post["id"] for post in posts], default=0) + 1

        new_post = {
            "id": new_id,
            "author": request.form.get("author"),
            "title": request.form.get("title"),
            "content": request.form.get("content")
        }

        posts.append(new_post)
        save_posts(posts)

        return redirect(url_for("index"))

    # Bei GET: Formular anzeigen
    return render_template("add.html")

@app.route('/delete/<int:post_id>')
def delete(post_id):
    posts = load_posts()

    # Filter: alle außer dem mit der ID
    posts = [post for post in posts if post["id"] != post_id]

    save_posts(posts)
    return redirect(url_for("index"))

@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    posts = load_posts()
    post = next((p for p in posts if p["id"] == post_id), None)

    if post is None:
        return "Post not found", 404

    if request.method == 'POST':
        post["author"] = request.form.get("author")
        post["title"] = request.form.get("title")
        post["content"] = request.form.get("content")
        save_posts(posts)
        return redirect(url_for("index"))

    return render_template("update.html", post=post)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
