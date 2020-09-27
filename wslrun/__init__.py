from .main import main
from pkg_resources import get_distribution

__version__ = get_distribution('foobar').version