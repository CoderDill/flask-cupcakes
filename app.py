from flask import Flask, json, request, jsonify, render_template
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


def serialize_cupcake(cupcake):
    """Serialize a cupcake SQLAlchemy obj to dict"""

    return {
        "id": cupcake.id,
        "flavor": cupcake.flavor,
        "size": cupcake.size,
        "rating": cupcake.rating,
        "image": cupcake.image
    }

@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/api/cupcakes")
def list_all_cupcakes():
    """Return JSON {'cupcakes': [{id, flavor, size, rating, image}, ...]"""

    all_cupcakes = [serialize_cupcake(cupcake)
                    for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)


@app.route("/api/cupcakes/<int:id>")
def list_single_cupcake(id):
    """Return JSON {'cupcakes': {id, flavor, size, rating, image}}"""

    cupcake = Cupcake.query.get_or_404(id)
    serialized = serialize_cupcake(cupcake)
    return jsonify(cupcake=serialized)


@app.route("/api/cupcakes", methods=["GET", "POST"])
def create_cupcake():
    """Create cupcake from form data & return it.
    Returns JSON {'dessert': {id, name, calories}}
    """

    flavor = request.json["flavor"]
    size = request.json["size"]
    rating = request.json["rating"]
    image = request.json["image"]

    new_cupcake = Cupcake(flavor=flavor, size=size, rating=rating, image=image)

    db.session.add(new_cupcake)
    db.session.commit()

    response_json = jsonify(cupcake=new_cupcake.serialize())

    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods=["PATCH"])
def update_cupcake(id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(id)

    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)

    # db.session.query(Cupcake).filter_by(id=id).update(request.json)
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())


@app.route('/api/cupcakes/<int:id>', methods=["DELETE"])
def delete_cupcake(id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
