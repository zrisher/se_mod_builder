import os
import psutil
import time


SE_PROCESS_NAMES = [
    "SpaceEngineers.exe", "SpaceEngineersDedicated.exe", "LoadARMS.exe"
]


def await_processes_killed():
    for process in psutil.process_iter():
        if process.name() in SE_PROCESS_NAMES:
            try:
                while process.status() != psutil.STATUS_DEAD:
                    print('Waiting on "{}" to exit.'.format(process.name()))
                    time.sleep(1)
            except psutil.NoSuchProcess:
                pass

    print('SE processes killed.')


def kill_processes():
    print('Killing SE processes.')
    for process in psutil.process_iter():
        if process.name() in SE_PROCESS_NAMES:
            print("Killing process:", process.name())
            process.kill()


def start_process(se_exe_path):
    print('Starting SE at "{}"'.format(se_exe_path))
    os.system('"{}"'.format(se_exe_path))
