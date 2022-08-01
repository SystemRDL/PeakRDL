# type: ignore
import sys

if sys.version_info >= (3,10,0):
    from importlib import metadata

    def get_entry_points(group_name):
        return metadata.entry_points().select(group=group_name)

elif sys.version_info >= (3,8,0):
    from importlib import metadata

    def get_entry_points(group_name):
        return metadata.entry_points().get(group_name, tuple())

else:
    import pkg_resources
    def get_entry_points(group_name):
        return pkg_resources.iter_entry_points(group_name)
