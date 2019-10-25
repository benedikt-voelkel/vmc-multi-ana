import os
import subprocess
from chep_utils.logger import get_logger
from chep_utils.io import print_dict, yaml_from_dict, make_dir

def make_scenario_suffix(*args):
    return "_".join(args)

def run_sim_test(config):

    logger = get_logger()
    logger.info("Run in test mode")

    output = os.path.join(config["output_path"], "test")
    make_dir(output)
    logger.info("Output written to %s", output)

    exec_list = [config["exec_path"], "--engine1", "G3", "--n-events", "5", "--macros",
                 config["macros_path"], "--pdg", "11", "--energy", "0.050"]
    succ = -1
    log_file = os.path.join(output, "test.log")
    with open(log_file, "w") as f:
        p = subprocess.Popen(exec_list, stdout=f, stderr=f)
        succ = p.wait()
    if succ >= 0:
        logger.info("SUCCESS code: %i", succ)


def run_sim_all(config):

    logger = get_logger()
    logger.info("Start full run with parameters")
    print_dict(config)

    # Fix the calo length
    fix_length = config["fix_length"]
    gap_size = config["gap_size"]
    abso_size = config["abso_size"]

    scenario_index = -1
    make_dir(config["output_path"])

    exec_list = [config["exec_path"], "--engine1", config["engine1"]]
    if config["engine2"] is not None:
        exec_list.extend(["--engine2", config["engine2"]])

    for nev in config["n_events"]:
        for nl in config["n_layers"]:
            gap_size_tmp = gap_size
            abso_size_tmp = abso_size
            if fix_length > 0.:
                layer_size = fix_length / nl
                gap_rel_size = gap_size / (gap_size + abso_size)
                abso_rel_size = 1. - gap_rel_size
                gap_size_tmp = gap_rel_size * layer_size
                abso_size_tmp = abso_rel_size * layer_size
                if max(gap_tmp_size, abso_tmp_size) < config["min_layer_size"]:
                    logger.warning("Minimum layer size reached for %i layers which is %f. Skip...",
                                   nl, config["min_layer_size"])
                    continue
            for npr in config["n_primaries"]:
                scenario_index += 1
                trial_index = -1
                yaml_dict = {"parameters": {"n_events": nev, "n_layers": nl, "n_primaries": npr,
                                            "engine1": config["engine1"], "engine2": config["engine2"],
                                            "pdg": config["pdg"], "energy": config["energy"]}}
                trials = []
                logger.info("Start scenario with")
                print_dict(yaml_dict)

                for ntr in range(config["trials"]):
                    logger.debug("Trial %i", ntr+1)
                    trial_index += 1
                    exec_list_run = exec_list + ["--n-events", str(nev), "--n-layers", str(nl),
                                                 "--n-primaries", str(npr), "--macros", config["macros_path"],
                                                 "--pdg", str(config["pdg"]), "--energy", str(config["energy"])]
                    succ = -1
                    log_file = os.path.join(config["output_path"], f"trial_{scenario_index}_{trial_index}.log")
                    with open(log_file, "w") as f:
                        p = subprocess.Popen(exec_list_run, stdout=f, stderr=f)
                        succ = p.wait()
                    single_trial = {"success": False, "time": -1., "log": log_file}
                    if succ >= 0:
                        single_trial["success"] = True
                        with open(log_file, "r") as f:
                            for line in f:
                                if line.find("segmentation violation") > -1:
                                    logger.error("Apparently there was a seg-fault in %s. Skip...", log_file)
                                    break
                                if line.find("### time elapsed (ns)") > -1:
                                    time = line.split(" ")
                                    single_trial["time"] = time[-1]
                                    break
                    # Append to trials
                    trials.append(single_trial)
                yaml_dict["trials"] = trials
                scenario_yaml = f"scenario_{scenario_index}.yaml"
                scenario_yaml = os.path.join(config["output_path"], scenario_yaml)
                yaml_from_dict(yaml_dict, scenario_yaml)

def run_sim(config):

    if config["test"]:
        run_sim_test(config)
        return

    run_sim_all(config)

