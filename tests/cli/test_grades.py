from unittest.mock import patch

from click.testing import CliRunner

from tests.cli import MockResponseBuilder, import_module

cv = import_module("cv", "cli/classeviva")


@patch(
    "requests.Session.post",
    side_effect=MockResponseBuilder("cli/testdata/identity.json"),
)
@patch(
    "requests.Session.get",
    side_effect=MockResponseBuilder("cli/testdata/grades.partial.json"),
)
def test_list_grades(identity_response_mock, grades_response_mock):
    runner = CliRunner()
    result = runner.invoke(cv.cli, ["list-grades"])

    expected = """
2022-03-17
- PERCUSSIONI, 8+
2021-11-04
- SECONDA LINGUA COMUNITARIA, 4 (blue)
"""

    assert result.exit_code == 0
    assert result.output == expected
