
import sh
import click
import sys
import os
from .device import device_list
from .utils import cd, copy_func

# UIAutomation Instruments Template location. Accurate as at Xcode 6.3
INSTRUMENTS_AUTOMATION_TEMPLATE_PATH = "/Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate" # DO NOT CHANGE INDENTATION!
FIXXD_FILENAME = ".fixxd"

@click.group()
def fixxd():
    pass

def get_config_dir(current_dir):
    file = os.path.join(current_dir, FIXXD_FILENAME)

    if os.path.exists(file):
        return current_dir

    if os.path.ismount(current_dir):
        return None

    parent = os.path.abspath(os.path.join(current_dir, "../"))
    if os.path.exists(parent):
        return get_config_dir(parent)

    return None

def test(app_name, js_path, result_dir = None, device = None):
    print("Finding folder from {0}".format(os.getcwd()))
    config_dir = get_config_dir(os.getcwd())
    print("Config_dir: {0}".format(config_dir))
    #TODO: Use config dir

    if not device:
        devices = device_list()
        if len(devices) == 0:
            raise Exception("Please plug a device")
        device = devices[0]

    if not result_dir:
        result_dir = os.path.join(os.path.dirname(__file__), "../../", "tmp")

    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    with cd(result_dir):
        #TODO: Compile coffee script to js
        #TODO: Copy js to tmp/build dir
        sh.instruments("-w", device,
                       "-t", INSTRUMENTS_AUTOMATION_TEMPLATE_PATH,
                       app_name,
                       "-e", "UIASCRIPT", js_path,
                       "-e", "UIARESULTSPATH", result_dir,
                       _out=sys.stdout, _err=sys.stderr)

@click.command()
@click.argument("app_name")
@click.argument("js_path")
@click.argument("device", default=None, required=False)
@click.argument("result_dir", default=None, required=False)
def cli_test(*args, **kwargs):
    test(*args, **kwargs)

fixxd.add_command(cli_test, "test")
