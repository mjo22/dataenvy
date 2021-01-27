import sys
from . import visualize_io as io
from . import visualize_plot as plot
from . import visualize_process as process

__all__ = ['io', 'plot', 'process']

sys.modules['visualize.io'] = sys.modules['visualize.visualize_io']
sys.modules['visualize.plot'] = sys.modules['visualize.visualize_plot']
sys.modules['visualize.process'] = sys.modules['visualize.visualize_process']
