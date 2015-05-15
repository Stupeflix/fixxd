
import sh
import click
import sys
import os
from .device import list_devices
from .utils import cd, copy_func

# UIAutomation Instruments Template location. Accurate as at Xcode 6.0.1.
INSTRUMENTS_AUTOMATION_TEMPLATE_PATH = "/Applications/Xcode.app/Contents/Applications/Instruments.app/Contents/PlugIns/AutomationInstrument.xrplugin/Contents/Resources/Automation.tracetemplate" # DO NOT CHANGE INDENTATION!

@click.group()
def fixxd():
    pass

def test(app_name, js_path, result_dir = None, device = None):
    if not device:
        devices = list_devices()
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
def cli_test():
    test(*args, **kwargs)

fixxd.add_command(cli_test, "test")
