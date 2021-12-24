from typing import List, Tuple
from bs4 import BeautifulSoup

import requests


def fetch_sample_io(problem_id: int) -> List[Tuple[str, str]]:
    """Fetch sample IO from BOJ website

    Parameters
    ----------
    problem_id
        The ID of the problem to get samples from.

    Returns
    -------
    List[Tuple[str, str]]
        List of input/output pairs.
    """
    req = requests.get(f"https://www.acmicpc.net/problem/{problem_id}")
    soup = BeautifulSoup(req.text, "html.parser")
    sample_input_tags = soup.find_all(
        "pre", id=lambda x: x != None and x.startswith("sample-input-")
    )
    sample_output_tags = soup.find_all(
        "pre", id=lambda x: x != None and x.startswith("sample-output-")
    )
    sample_inputs = [x.text for x in sorted(sample_input_tags, key=lambda x: x.get("id"))]  # type: ignore
    sample_outputs = [x.text for x in sorted(sample_output_tags, key=lambda x: x.get("id"))]  # type: ignore
    return list(zip(sample_inputs, sample_outputs))
