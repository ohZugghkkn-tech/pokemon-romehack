from concurrent.futures import ThreadPoolExecutor
import unittest
from unittest.mock import patch

from tools.soulgold_docs.c_parser import preprocess_source


class PreprocessorTests(unittest.TestCase):
    def test_parallel_inputs_are_isolated(self):
        def preprocess_value(value):
            return preprocess_source(f"#define VALUE {value}\nVALUE\n").strip()

        with ThreadPoolExecutor(max_workers=8) as executor:
            results = list(executor.map(preprocess_value, range(32)))
        self.assertEqual(results, [str(value) for value in range(32)])

    def test_stdin_and_extra_include_path(self):
        with patch("tools.soulgold_docs.c_parser.subprocess.run") as run:
            run.return_value.returncode = 0
            run.return_value.stdout = "result"
            self.assertEqual(preprocess_source("source", "extra"), "result")
        args, kwargs = run.call_args
        self.assertIn("-x", args[0])
        self.assertIn("-Iextra", args[0])
        self.assertEqual(args[0][5], "-")
        self.assertEqual(kwargs["input"], "source")

    def test_invalid_source_fails(self):
        with self.assertRaisesRegex(RuntimeError, "deliberate_error"):
            preprocess_source("#error deliberate_error\n")
