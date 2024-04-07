from flask import Flask, render_template, request, Response

import json

from dict_generator.generator import (
    FrequencyBasedKeyGenerator,
    SchemaBasedDictGenerator,
)

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        names = request.form.getlist("name[]")
        types = request.form.getlist("type[]")
        frequencies = request.form.getlist("frequency[]")
        values_lists = request.form.getlist("values[]")

        schema = {}
        dist_schema = {}
        for name, type_, frequency, values in zip(
            names, types, frequencies, values_lists
        ):
            schema[name] = {
                "type": type_,
                "frequency": frequency,
                "values": list(
                    map(
                        {"int": int, "float": float}.get(type_, lambda x: x),
                        values.split(","),
                    )
                ),
            }
            dist_schema[name] = float(frequency) / 100

        count = request.form.get("count") or 100

        def generate():
            key_generator = FrequencyBasedKeyGenerator(int(count), dist_schema)
            dict_generator = SchemaBasedDictGenerator(schema)
            for item in key_generator:
                # Replace this with your actual data generation logic
                data = dict_generator.generate(item)
                yield json.dumps(data) + "\n"

        return Response(generate(), mimetype="application/json")
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
