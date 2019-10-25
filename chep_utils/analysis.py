import argparse
from chep_utils.run import run
from chep_utils.logger import configure_logger
from chep_utils.config import make_config

def main():
    """
    This is used as the entry point for ml-analysis.
    Read optional command line arguments and launch the analysis.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="activate debug log level")
    parser.add_argument("--log-file", dest="log_file", help="file to print the log to")
    parser.add_argument("--run-config", "-r", dest="run_config",
                        help="the run configuration to be used")
    parser.add_argument("--test", action="store_true", dest="test",
                        help="steer a test run")
    parser.add_argument("--trials", type=int, help="how many trial to be done")
    parser.add_argument("--mode", help="mode (single, multi)")
    parser.add_argument("--engine1", help="first engine")
    parser.add_argument("--engine2", help="second engine")
    parser.add_argument("--output-path", dest="output_path", help="output to be written")
    parser.add_argument("--exec-path", dest="exec_path", help="where to find executable")
    parser.add_argument("--macros-path", dest="macros_path", help="where to find additional macros to be loaded")
    parser.add_argument("--pdg", help="particle PDG")
    parser.add_argument("--energy", help="particle energy (GeV)")
    parser.add_argument("--fix-length", dest="fix_length", help="use fixed length")
    parser.add_argument("--min-layer-size", dest="min_layer_size", help="minimal thickness of layer")

    args = parser.parse_args()

    configure_logger(args.debug, args.log_file)

    config = make_config(args.run_config, trials=args.trials, mode=args.mode, engine1=args.engine1,
                         engine2=args.engine2, test=args.test, output_path=args.output_path,
                         exec_path=args.exec_path, macros_path=args.macros_path, pdg=args.pdg,
                         energy=args.energy, fix_length=args.fix_length, min_layer_size = args.min_layer_size)

    print(config)
    exit(0)
    # Run the chain
    run(config)

