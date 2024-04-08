import time
import unittest

from src.dict_generator.generator import (
    FrequencyBasedKeyGenerator,
    SchemaBasedDictGenerator,
)


class TestFrequencyBaseKeyGeneratorMixin:
    count: int = 100_000
    percentages: list[float] = [0.5, 0.5, 0.5]

    def test_generator(self):
        keys = ["first_key", "second_key", "third_key"]
        schema = {
            "first_key": {
                "type": "int",
                "values": [1, 10],  # Generate integers between 1 and 10
            },
            "second_key": {
                "type": "float",
                "values": [0, 1],  # Generate floats between 0 and 1
            },
            "third_key": {
                "type": "choice",
                "values": ["a", "b", "c"],  # Choose randomly from 'a', 'b', 'c'
            },
        }

        dict_generator = SchemaBasedDictGenerator(schema)
        generator = FrequencyBasedKeyGenerator(
            self.count, dict(zip(keys, self.percentages))
        )
        start = time.time()
        for dictionary in generator:
            # suppress the output
            # print(dict_generator.generate(dictionary))
            _ = dict_generator.generate(dictionary)
        print(time.time() - start)


class StressTestFrequencyBaseKeyGeneratorTier1(
    TestFrequencyBaseKeyGeneratorMixin, unittest.TestCase
):
    count = 100
    percentages = [0.5, 0.5, 0.5]


class StressTestFrequencyBaseKeyGeneratorTier2(
    TestFrequencyBaseKeyGeneratorMixin, unittest.TestCase
):
    count = 1_000
    percentages = [0.5, 0.3, 0.1]


class StressTestFrequencyBaseKeyGeneratorTier3(
    TestFrequencyBaseKeyGeneratorMixin, unittest.TestCase
):
    count = 10_000
    percentages = [0.1, 0.1, 0.1]


class StressTestFrequencyBaseKeyGeneratorTier4(
    TestFrequencyBaseKeyGeneratorMixin, unittest.TestCase
):
    count = 100_000
    percentages = [0.9, 0.9, 0.9]


class StressTestFrequencyBaseKeyGeneratorTier5(
    TestFrequencyBaseKeyGeneratorMixin, unittest.TestCase
):
    count = 1_000_000
    percentages = [0.5, 0.5, 0.9]


if __name__ == "__main__":
    unittest.main()
