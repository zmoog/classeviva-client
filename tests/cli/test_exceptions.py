from click.testing import CliRunner

from tests.cli import import_module

cv = import_module("cv", "cli/classeviva")


def test_exceptions():
    runner = CliRunner()
    result = runner.invoke(
        cv.cli,
        ["list-agenda", "--since", "2022-04-05", "--until", "2022-04-05"],
        env={
            # Setting environment variables for credentials to a
            # blank value is expected to cause the raise of a
            # `CredentialsNotFoundError` exception.
            "CLASSEVIVA_USERNAME": "",
            "CLASSEVIVA_PASSWORD": "",
        },
    )

    expected = (
        "Error: Can't find credentials in the "
        "CLASSEVIVA_* environment variables\n"
    )

    assert result.exit_code == 1
    assert result.output == expected
