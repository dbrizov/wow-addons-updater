from cx_Freeze import setup, Executable

setup(name="wow_addons_updater",
      description="WoW Addons Updater",
      executables=[Executable("wow_addons_updater.py")])

# To create a build
# 1. Install cx_Freeze (pip install cx_Freeze)
# 2. Run the following in the console "python setup.py build"
