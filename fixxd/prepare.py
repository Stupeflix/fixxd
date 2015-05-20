import coffeescript
import sh
from os import path, listdir
from .utils import logger


def prepare_file(file_path, build_dir):
    """ Move file into build folder before launching actual command (also compile coffeescript) """
    logger.info("Preparing file {0}".format(file_path))
    if file_path.endswith(".coffee"):
        logger.info("Compiling coffee script")
        f = open(file_path, 'r')
        js_content = ""
        coffee_content = ""
        for line in f:
            content_to_add = "{0}\n".format(line)
            if line.strip().startswith("#import"):
                js_content += content_to_add
            else:
                coffee_content += content_to_add

        compiled_content = coffeescript.compile(coffee_content).split('\n')

        js_content += '\n'.join(compiled_content[1:-2])

        logger.debug(js_content)
        file_name = path.splitext(path.basename(file_path))[0] + ".js"
        build_path = path.join(build_dir, file_name)
        f = open(build_path, 'w')
        f.write(js_content)
        return build_path
    else:
        logger.info("Copy JS file to build dir")
        build_path = path.join(build_dir, path.basename(file_path))
        sh.cp(file_path, build_path)

        return build_path


def prepare_lib(lib_dir, build_dir):
    logger.info("Preparing lib from {0} to {1}".format(lib_dir, build_dir))
    sh.rsync("-avz", "--delete", lib_dir, build_dir)
    recurse_compile(build_dir)


def recurse_compile(directory):
    logger.info("Compiling lib coffee scripts")
    for f in listdir(directory):
        f_path = path.join(directory, f)
        if path.isfile(f_path):
            if f.endswith(".coffee"):
                prepare_file(f_path, directory)
                sh.rm(f_path)
        elif path.isdir(f_path):
            recurse_compile(f_path)
