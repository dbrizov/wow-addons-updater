from cx_Freeze import setup, Executable

setup(name="wow_addons_updater",
      description="WoW Addons Updater",
      executables=[Executable("wow_addons_updater.py")])

# To create a build run the following in the console
# > python setup.py build
