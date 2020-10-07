from shipping import __version__
from shipping.commands import Process


def test_run_main():
    python_process = Process("python")
    call = ["-m", "shipping", "--version"]
    python_process.run_command(call)
    assert __version__ in python_process.stdout
