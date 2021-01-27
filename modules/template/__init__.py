import sys
from . import GREENELEPHANT_io as io
from . import GREENELEPHANT_plot as plot
from . import GREENELEPHANT_process as process

__all__ = ['io', 'plot', 'process']

sys.modules['GREENELEPHANT.io'] = sys.modules['GREENELEPHANT.GREENELEPHANT_io']
sys.modules['GREENELEPHANT.plot'] = sys.modules['GREENELEPHANT.GREENELEPHANT_plot']
sys.modules['GREENELEPHANT.process'] = sys.modules['GREENELEPHANT.GREENELEPHANT_process']
