# -*- coding: utf-8 -*-
import logging
import signal
import subprocess

log = logging.getLogger(__name__)

CLI_OPTIONS = {
    'family': {'option': '--family_id'},
    'config': {'option': '--config_file'},
    'priority': {'option': '--slurm_quality_of_service'},
    'email': {'option': '--email'},
    'base': {'option': '--cluster_constant_path'},
    'dryrun': {
        'option': '--dry_run_all',
        'default': '2',
    },
    'gene_list': {'option': '--vcfparser_select_file'},
    'max_gaussian': {
        'option': '--gatk_variantrecalibration_snv_max_gaussians',
        'default': '1',
    },
}


class MipCli(object):

    """Wrapper around MIP command line interface."""

    def __init__(self, script):
        """Initialize MIP command line interface."""
        self.script = script

    def __call__(self, config, family, **kwargs):
        """Execute the pipeline."""
        command = self.build_command(config, family=family, **kwargs)
        process = self.execute(command)
        process.wait()
        if process.returncode != 0:
            log.error("error starting analysis, check the output")
        return process

    def build_command(self, config, **kwargs):
        """Builds the command to execute MIP."""
        command = ['perl', self.script, CLI_OPTIONS['config']['option'], config]
        for key, value in kwargs:
            command.append(CLI_OPTIONS[key]['option'])
            if value is True:
                command.append(CLI_OPTIONS[key]['default'])
            else:
                command.append(value)
        return command

    def execute(self, command):
        """Start a new MIP run."""
        process = subprocess.Popen(
            command,
            preexec_fn=lambda: signal.signal(signal.SIGPIPE, signal.SIG_DFL)
        )
        return process
