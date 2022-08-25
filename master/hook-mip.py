''' This program is a hook for Pyinstaller.
It allows the import of python-mip library. Without it, the library cannot be imported
and executable cannot be created with Pyinstaller.'''

from PyInstaller.utils.hooks import collect_dynamic_libs

binaries = collect_dynamic_libs('mip')
