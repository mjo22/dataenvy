import sys
from . import pdf_io as io
from . import pdf_plot as plot
from . import pdf_process as process

__all__ = ['io', 'plot', 'process']

sys.modules['pdf.io'] = sys.modules['pdf.pdf_io']
sys.modules['pdf.plot'] = sys.modules['pdf.pdf_plot']
sys.modules['pdf.process'] = sys.modules['pdf.pdf_process']
