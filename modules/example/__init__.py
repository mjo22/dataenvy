import sys
from . import example_io as io
from . import example_plot as plot
from . import example_process as process

__all__ = ['io', 'plot', 'process']

sys.modules['example.io'] = sys.modules['example.example_io']
sys.modules['example.plot'] = sys.modules['example.example_plot']
sys.modules['example.process'] = sys.modules['example.example_process']
