import sh

def list_devices():
    #TODO: separate iPhone and iPad
    raw = sh.sed(sh.system_profiler("SPUSBDataType"), "-n", "-e", '/iPad/,/Serial/p', "-e", '/iPhone/,/Serial/p')
    devices = sh.awk(sh.grep(raw, "Serial Number:"), "-F",": ", "{print $2}").split('\n')
    return [device for device in devices if device]
