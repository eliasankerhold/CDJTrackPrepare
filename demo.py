from handling_lib import LibraryManager
from supported_files import cdj_nxs_2000_specs

lib_source = "F:\\TRACKS"

lib_manager = LibraryManager(source_lib=lib_source, mode='replace', cdj_specs=cdj_nxs_2000_specs)
lib_manager.scrape_library()
lib_manager.diagnose_library()
input('Press Enter to fix library...')
lib_manager.fix_library()