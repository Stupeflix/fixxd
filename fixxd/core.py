
import sh
import click
import sys
from os import path, getcwd, makedirs
from .device import device_list
from .utils import cd, logger
from .config import get_config
from .prepare import prepare_file, prepare_lib

# UIAutomation Instruments Template location. Accurate as at Xcode 6.3
INSTRUMENTS_AUTOMATION_TEMPLATE_PATH = "/Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate"


@click.group()
def fixxd():
    pass


def test(test_file, device=None, verbose=False, debug=False):
    """
    Launch UI Automation tests from `test_file` on device `device` using instruments.
    """
    logger.debug("Finding folder from {0}".format(getcwd()))

    if verbose is True:
        logger.setLevel("INFO")
    if debug is True:
        logger.setLevel("DEBUG")

    cfg = get_config(getcwd())

    if not cfg:
        raise Exception("You must be in a fixxd folder")

    if not device:
        devices = device_list()
        if len(devices) == 0:
            raise Exception("Please plug a device")
        device = devices[0]

    results_dir = cfg["results_dir"]
    if not path.exists(results_dir):
        makedirs(results_dir)

    build_dir = cfg["build_dir"]
    if not path.exists(build_dir):
        makedirs(build_dir)

    # TODO: Detect device from CLI, test_file is meant to become a name only  (test_name)
    device_dir_name = path.dirname(test_file)

    build_dir_with_device = path.join(build_dir, device_dir_name)
    if not path.exists(build_dir_with_device):
        makedirs(build_dir_with_device)

    abs_test_path = path.abspath(path.join(cfg["tests_dir"], test_file))
    test_path = prepare_file(abs_test_path, build_dir_with_device)

    prepare_lib(cfg["lib_dir"], path.join(build_dir, "lib/"))

    with cd(results_dir):
        sh.instruments("-w", device,
                       "-t", INSTRUMENTS_AUTOMATION_TEMPLATE_PATH,
                       cfg["app_name"],
                       "-e", "UIASCRIPT", test_path,
                       "-e", "UIARESULTSPATH", results_dir,
                       _out=sys.stdout, _err=sys.stderr)


@click.command()
@click.argument("test-file")
@click.argument("device", default=None, required=False)
@click.option("--verbose", is_flag=True)
@click.option("--debug", is_flag=True)
def cli_test(*args, **kwargs):
    test(*args, **kwargs)

fixxd.add_command(cli_test, "test")
