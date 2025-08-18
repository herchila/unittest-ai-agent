"""Automated Unit Test Generation CLI with AI."""
import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH_SAMPLE_FUNCTION = os.path.join(
    BASE_DIR, "unittest_ai_agent", "example", "converter.py"
)
FILE_PATH_PROMPT = os.path.join(BASE_DIR, "prompts")
TEST_DIR_PATH = os.path.join(BASE_DIR, "example", "tests")
