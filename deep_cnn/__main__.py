import sys

from .logger import logger, set_file_handler
from .train_model import main
from .utils import argument_parser

opt = argument_parser(sys.argv[1:])

set_file_handler(logger, opt.run_name)

main(opt)
