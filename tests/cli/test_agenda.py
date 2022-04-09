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
    side_effect=MockResponseBuilder("cli/testdata/agenda.2022-04-05.json"),
)
def test_list_grades(identity_response_mock, agenda_response_mock):
    runner = CliRunner()
    result = runner.invoke(
        cv.cli,
        ["list-agenda", "--since", "2022-04-05", "--until", "2022-04-05"],
    )

    expected = """
2022-04-05
- DICEMBRE ELISA, VERIFICA DI GRAMMATICA
- GRIMALDI ALESSANDRO, Studiare Intermezzo da Cavalleria rusticana.
"""

    assert result.exit_code == 0, f"command failed due to: {result.output}"
    assert result.output == expected
