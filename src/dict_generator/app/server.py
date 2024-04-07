from flask import Flask, render_template, request, Response

import random
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

        count = request.form.get("count") or 1000
        kind = request.form.get("kind") or "pub"

        def generate():
            key_generator = FrequencyBasedKeyGenerator(int(count), dist_schema)
            dict_generator = SchemaBasedDictGenerator(schema)
            for item in key_generator:
                # Replace this with your actual data generation logic
                data = dict_generator.generate(item)
                yield json.dumps(data) + "\n"

        def generate_subscription():
            key_generator = FrequencyBasedKeyGenerator(int(count), dist_schema)
            dict_generator = SchemaBasedDictGenerator(schema)
            for item in key_generator:
                # Replace this with your actual data generation logic
                data = dict_generator.generate(item)
                result = []
                for key, value in data.items():
                    operand = "="
                    if schema[key]["type"] in ["int", "float"]:
                        operand = random.choice(["<", ">", "=", "<=", ">="])
                    # result.append((key, operand, value))
                    result.append(f"({key}, {operand}, {value})")

                yield "{" + ", ".join(result) + "}\n"

        def dummy_generate():
            key_generator = FrequencyBasedKeyGenerator(int(count), dist_schema)
            dict_generator = SchemaBasedDictGenerator(schema)
            result = ""
            for item in key_generator:
                # Replace this with your actual data generation logic
                data = dict_generator.generate(item)
                result = result + json.dumps(data) + "\n"
            yield result

        def dummy_generate_subscription():
            key_generator = FrequencyBasedKeyGenerator(int(count), dist_schema)
            dict_generator = SchemaBasedDictGenerator(schema)
            result_ = ""
            for item in key_generator:
                # Replace this with your actual data generation logic
                data = dict_generator.generate(item)
                result = []
                for key, value in data.items():
                    operand = "="
                    if schema[key]["type"] in ["int", "float"]:
                        operand = random.choice(["<", ">", "=", "<=", ">="])
                    # result.append((key, operand, value))
                    result.append(f"({key}, {operand}, {value})")

                result_ = result_ + "{" + ", ".join(result) + "}\n"
            yield result_

        if kind == "pub":
            return Response(generate(), mimetype="application/json")
        if kind == "sub":
            return Response(generate_subscription(), mimetype="application/json")
        if kind == "dummy_pub":
            return Response(dummy_generate(), mimetype="application/json")
        if kind == "dummy_sub":
            return Response(dummy_generate_subscription(), mimetype="application/json")

        return "Invalid kind of data"
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
