import argparse
from chep_utils.run import run_sim
from chep_utils.logger import configure_logger
from chep_utils.config import make_config

def run(args):
    configure_logger(args.debug, args.log_file)

    config = make_config(args.run_config, trials=args.trials, mode=args.mode, engine1=args.engine1,
                         engine2=args.engine2, test=args.test, output_path=args.output_path,
                         exec_path=args.exec_path, macros_path=args.macros_path, pdg=args.pdg,
                         energy=args.energy, fix_length=args.fix_length, min_layer_size = args.min_layer_size,
                         gap_size=args.gap_size, abso_size=args.abso_size)

    # Run the chain
    run_sim(config)

def main():
    """
    This is used as the entry point for ml-analysis.
    Read optional command line arguments and launch the analysis.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--debug", action="store_true", help="activate debug log level")
    parser.add_argument("--log-file", dest="log_file", help="file to print the log to")

    subparsers = parser.add_subparsers(help="available commands")

    parser_run = subparsers.add_parser("run")
    parser_run.set_defaults(func=run)
    parser_run.add_argument("--run-config", "-r", dest="run_config",
                        help="the run configuration to be used")
    parser_run.add_argument("--test", action="store_true", dest="test",
                        help="steer a test run")
    parser_run.add_argument("--trials", type=int, help="how many trial to be done")
    parser_run.add_argument("--mode", help="mode (single, multi)")
    parser_run.add_argument("--engine1", help="first engine")
    parser_run.add_argument("--engine2", help="second engine")
    parser_run.add_argument("--output-path", dest="output_path", help="output to be written")
    parser_run.add_argument("--exec-path", dest="exec_path", help="where to find executable")
    parser_run.add_argument("--macros-path", dest="macros_path", help="where to find additional macros to be loaded")
    parser_run.add_argument("--pdg", type=int, help="particle PDG")
    parser_run.add_argument("--energy", type=float, help="particle energy (GeV)")
    parser_run.add_argument("--fix-length", dest="fix_length", type=int, help="use fixed length")
    parser_run.add_argument("--min-layer-size", dest="min_layer_size", type=float, help="minimal thickness of layer")
    parser_run.add_argument("--gap-size", dest="gap_size", type=float, help="gap size")
    parser_run.add_argument("--abso-size", dest="abso_size", type=float, help="absorber size")

    #parser_ana = parser.add_subparser("analysis")

    args = parser.parse_args()

    args.func(args)


