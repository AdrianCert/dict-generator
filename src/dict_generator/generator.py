import math
import random
from typing import List


class FrequencyBasedKeyGenerator:
    def __init__(
        self,
        target_count,
        frequency_schema,
        non_empty: bool = True,
    ):
        self.target_count = target_count
        self.counts = {
            key: math.ceil(percentage * target_count)
            for key, percentage in frequency_schema.items()
        }
        self.compute_mandatory_counts()
        left_unfilled = self.mandatory_counts
        if non_empty and not left_unfilled:
            raise ValueError("The sum of the percentages is less than the target count")

    def compute_mandatory_counts(self):
        self.mandatory_counts = {}
        left_filling = self.target_count
        # Sort the keys based on their values in descending order
        sorted_keys = sorted(
            self.counts.keys(), key=lambda key: self.counts[key], reverse=True
        )

        # Assign the mandatory counts for each key in the sorted order
        for key in sorted_keys:
            count = self.counts[key]
            if left_filling >= count:
                self.mandatory_counts[key] = count
                self.counts[key] = 0
                left_filling -= count
            else:
                self.mandatory_counts[key] = left_filling
                self.counts[key] -= left_filling
                left_filling -= count
                break
        return left_filling

    def __iter__(self):
        return self

    def __next__(self):
        if not self.target_count:
            raise StopIteration

        self.target_count -= 1
        mandatory_key = random.choice(list(self.mandatory_counts))
        self.mandatory_counts[mandatory_key] -= 1
        if self.mandatory_counts[mandatory_key] == 0:
            del self.mandatory_counts[mandatory_key]
            if not self.mandatory_counts:
                # Stop the iteration
                self.target_count = 0

        result = [mandatory_key]
        for key, count in self.counts.items():
            if mandatory_key == key:
                continue
            if count == 0:
                continue
            left_opportunities = self.target_count - self.mandatory_counts.get(key, 0)

            if left_opportunities > count and random.random() > 0.9:  # noqa PLR2004
                continue
            result.append(key)
            self.counts[key] -= 1

        return result


class SchemaBasedDictGenerator:
    def __init__(self, schema):
        self.schema = schema

    def generate_int(self, values):
        return random.randint(*values)

    def generate_float(self, values):
        return random.uniform(*values)

    def generate_choice(self, values):
        return random.choice(values)

    def generate_item(self, key: str):
        schema = self.schema[key]
        func = getattr(self, f"generate_{schema['type']}")
        return func(schema["values"])

    def generate_items(self, keys_list: List[str]):
        for key in keys_list:
            yield key, self.generate_item(key)

    def generate(self, keys_list=None):
        keys_list = [
            key for key in keys_list or self.schema.keys() if key in self.schema
        ]
        return dict(self.generate_items(keys_list))


if __name__ == "__main__":
    import time

    # Usage
    keys = ["key1", "key2", "key3"]
    percentages = [0.5, 0.5, 0.5]
    schema = {
        "key1": {
            "type": "int",
            "values": [1, 10],  # Generate integers between 1 and 10
        },
        "key2": {
            "type": "float",
            "values": [0, 1],  # Generate floats between 0 and 1
        },
        "key3": {
            "type": "choice",
            "values": ["a", "b", "c"],  # Choose randomly from 'a', 'b', 'c'
        },
    }

    dict_generator = SchemaBasedDictGenerator(schema)
    generator = FrequencyBasedKeyGenerator(100_000, dict(zip(keys, percentages)))
    start = time.time()
    for dictionary in generator:
        # suppress the output
        # print(dict_generator.generate(dictionary))
        _ = dict_generator.generate(dictionary)

    print(time.time() - start)
