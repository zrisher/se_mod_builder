def start_builds(models_dir, mwm_exe_path):
    """
    start mwmBuilder processes in parallel
    TODO
    """
    print('Starting model builds.')
    """
    mwm_processes = []
    print("looking for model dirs to build from")

    for model_dir_name in model_dir_names:
        for size_dir_name in size_dir_names:
            models_path = os.path.join(
                models_dir, model_dir_name, size_dir_name
            )
            if os.path.exists(models_path):
                print("spawning process for " + models_path)

                mwm_processes.append(
                    subprocess.Popen(
                        ["python", model_process_path],
                        cwd=models_path, mwm_path=mwm_path
                    )
                )

    return mwm_processes

    print("--- Starting MWM Model Builder Threads --- ")
    mwm_processes = lib.build.process_models(
        source_modules, build_model_path, mwm_builder_path
    )
    mwm_processes_count = mwm_processes.__len__()
    if mwm_processes_count > 0:
        print("Running {0} mwm_processes.".format(mwm_processes.__len__()))
    else:
        print("no mwm_processes running")
    print("")
    """
    """
    # This scripts builds all the .FBX files in the current directory into
    # .mwm files using MwmBuilder.exe
    # You will get Texture warnings while running this script.
    #
    # the path to MwmBuilder.exe may be supplied:
    #		as the first argument
    #		in build.ini, which must be in the same directory as this script
    # failing that, this script will test for MwmBuilder.exe in this script's
    # directory
    # failing that, this script will test for MwmBuilder.exe in the current
    # working directory
    scriptDir = os.path.dirname(os.path.realpath(sys.argv[0]))
    buildIni = scriptDir + "\\build.ini"
    startDir = os.getcwd()
    input = "MwmBuilder\\Content"
    output = input + "\\Output"

    exe_path = global_config.se_steam_dir + r"\Tools\MwmBuilder\MwmBuilder.exe"

    # test current directory contains fbx and xml files
    bNoFBX = True
    bNoXML = True
    for file in os.listdir('.'):
      if file.lower().endswith(".fbx"):
        bNoFBX = False
      else:
        if file.lower().endswith(".xml"):
          bNoXML = False

    if bNoFBX or bNoXML:
      print("WARNING: " + os.getcwd() + " does not contain .fbx and .xml
      files")
      sys.exit()


    def createDir(l_dir):
      if not os.path.exists(l_dir):
        os.makedirs(l_dir)

    # delete all the files in a directory
    def emptyDir(l_dir):
      if os.path.exists(l_dir):
        for file in os.listdir(l_dir):
          if os.path.isfile(l_dir + "\\" + file):
            os.remove(l_dir + "\\" + file)

    def copyWithExtension(l_from, l_to, l_ext):
      createDir(l_to)
      os.chdir(l_from)
      for file in os.listdir('.'):
        if file.lower().endswith(l_ext.lower()):
          shutil.copy2(file, l_to)


    # set up directories for MwmBuilder
    emptyDir(startDir + "\\" + input)
    emptyDir(startDir + "\\" + output)
    createDir(input)
    createDir(output)
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

    # cannot delete directories, but we can empty them
    emptyDir(startDir + "\\" + input)
    emptyDir(startDir + "\\" + output)

        TODO: Wait for MWM Builder to complete before distributing models
    if mwm_processes_count > 0:
        print("waiting for our mwm processes to finish")
        for mwm_process in mwm_processes:
            mwm_process.wait()


    """
    """
        # test current directory contains fbx and xml files
    bNoFBX = True
    bNoXML = True
    for file in os.listdir('.'):
        if file.lower().endswith(".fbx"):
            bNoFBX = False
        else:
            if file.lower().endswith(".xml"):
                bNoXML = False

    if bNoFBX or bNoXML:
        print(
            "WARNING: " + os.getcwd() + " does not contain .fbx and .xml
            files")
        sys.exit()


    # set up directories for MwmBuilder
    createDir(input)
    createDir(output)
    copyWithExtension(startDir, input, ".fbx")
    copyWithExtension(startDir, input, ".hkt")
    copyWithExtension(startDir, output,
                      ".mwm")  # copying.mwm to output allows MwmBuilder to
                      skip unchanged models
    copyWithExtension(startDir, input, ".xml")

    # run MwmBuilder
    mwmBuilderProcess = subprocess.Popen(
        [mwmBuilder, "/s:" + input, "/o:" + output,
         "/l:" + startDir + "\\MwmBuilder.log"])
    mwmBuilderProcess.wait()
    copyWithExtension(output, startDir, ".mwm", True)

    # cannot delete directories, but we can empty them
    emptyDir(startDir + "\\" + input)
    emptyDir(startDir + "\\" + output)
    """
    return []


def await_builds(builds):
    """
    TODO
    """
    print('Finished model builds.')
    return None
