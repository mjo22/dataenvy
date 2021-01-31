import sys
from . import PLACEHOLDER_io as io
from . import PLACEHOLDER_plot as plot
from . import PLACEHOLDER_process as process

__all__ = ['io', 'plot', 'process']

sys.modules['PLACEHOLDER.io'] = sys.modules['PLACEHOLDER.PLACEHOLDER_io']
sys.modules['PLACEHOLDER.plot'] = sys.modules['PLACEHOLDER.PLACEHOLDER_plot']
sys.modules['PLACEHOLDER.process'] = sys.modules['PLACEHOLDER.PLACEHOLDER_process']
