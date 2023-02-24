# EXPERIMENTAL REDESIGNED LAUNCHER
import Launcher_Utils
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=1,thread_name_prefix='SLAY') as exec:
    Launcher_Utils.MainWindow(exec)