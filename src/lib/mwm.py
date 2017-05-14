import os


def start_builds(models_dir, mwm_exe_path):
    """
    start mwmBuilder processes in parallel
    TODO
    """
    print('Starting model builds.')

    mwm_processes = []
    # make tmp input/output dirs

    for dir_path, dir_names, file_names in os.walk(models_dir):
        for file_name in file_names:
            if file_name.lower().endswith(".fbx"):
                # must have .xml file too, possible hkt collision model
                # start build model with those files and tmp paths
                # add its resulting process to processes
                """
                # You will get Texture warnings while running this script.

                # set up directories for MwmBuilder
                copyWithExtension(startDir, input, ".fbx")
                copyWithExtension(startDir, input, ".xml")
                copyWithExtension(startDir, input, ".hkt")
                copyWithExtension(startDir, output, ".mwm") # copying.mwm to output allows
                MwmBuilder to skip unchanged models

                # run MwmBuilder
                mwmBuilderProcess = subprocess.Popen([mwmBuilder, "/s:" + input, "/o:" +
                output, "/l:" + startDir + "\\MwmBuilder.log"])
                mwmBuilderProcess.wait()
                copyWithExtension(output, startDir, ".mwm")
                """
                continue

    return mwm_processes


def await_builds(builds):
    for build in builds:
        build.wait()
    print('Finished model builds.')
