import sys
from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from importlib.metadata import EntryPoint, Distribution

if sys.version_info >= (3,10,0):
    from importlib import metadata

    def _get_entry_points(group_name: str) -> List[Tuple['EntryPoint', 'Distribution']]:
        eps = []
        for ep in metadata.entry_points().select(group=group_name):
            eps.append((ep, ep.dist))
        return eps

    def _get_name_from_dist(dist: 'Distribution') -> str:
        return dist.name

elif sys.version_info >= (3,8,0):
    from importlib import metadata

    def _get_entry_points(group_name: str) -> List[Tuple['EntryPoint', 'Distribution']]:
        eps = []
        for dist in metadata.distributions():
            for ep in dist.entry_points:
                if ep.group == group_name:
                    eps.append((ep, dist))
        return eps

    def _get_name_from_dist(dist: 'Distribution') -> str:
        return dist.metadata["Name"]

else:
    import pkg_resources # type: ignore

    def _get_entry_points(group_name: str) -> List[Tuple['EntryPoint', 'Distribution']]:
        eps = []
        for ep in pkg_resources.iter_entry_points(group_name):
            eps.append((ep, ep.dist))
        return eps

    def _get_name_from_dist(dist: 'Distribution') -> str:
        return dist.project_name # type: ignore


def get_entry_points(group_name: str) -> List[Tuple['EntryPoint', 'Distribution']]:
    return _get_entry_points(group_name)

def get_name_from_dist(dist: 'Distribution') -> str:
    return _get_name_from_dist(dist)
