# script for use with snakemake
import sys
import os
import subprocess
import traceback
from bifrostlib import datahandling


def rule__run_cge_pointfinder(input, sampleComponentObj, log):
    try:
        this_function_name = sys._getframe().f_code.co_name
        name, options, resources = sampleComponentObj.start_rule(this_function_name, log=log)

        provided_specie = sampleComponentObj.get_sample_properties_by_category("sample_info")['provided_species']
        species_mapping = options["species_mapping"]

        # Code to run
        if provided_specie not in species_mapping:
            sampleComponentObj.write_log_out(log, "species {} not in mlst species\n".format(provided_specie))
            sampleComponentObj.rule_run_cmd("touch {}/specie_DB".format(name), log)
        else:
            organism = species_mapping[provided_specie][0]
            sampleComponentObj.rule_run_cmd("/bifrost_resources/pointfinder/PointFinder.py -i {} -o {} -s {} -p /bifrost/cge_pointfinder_kma/pointfinder_db -m kma -m_p /opt/conda/pkgs/kma-1.3.0-hed695b0_0/bin/kma".format(
            input.reads, os.path.join(name, "resistance"), organism), log)

        sampleComponentObj.end_rule(this_function_name, log=log)
    except Exception:
        sampleComponentObj.write_log_err(log, str(traceback.format_exc()))


rule__run_cge_pointfinder(
    snakemake.input,
    snakemake.params.sampleComponentObj,
    snakemake.log)
