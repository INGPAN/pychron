# ===============================================================================
# Copyright 2011 Jake Ross
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================



"""
Global path structure

add a path verification function
make sure directory exists and build if not
"""
from os import path, mkdir

# host_url = 'https://arlab.googlecode.com/svn'
# project_root = 'trunk'

# if beta:
#    home = '{}_beta{}'.format(home, version)
#    project_root = 'branches/pychron'
#
# project_home = join(host_url, project_root)
import os


class Paths():
    dissertation = '/Users/ross/Programming/git/dissertation'
    enthought = path.join(path.expanduser('~'), '.enthought')
    users_file = path.join(enthought, 'users')
    base = path.expanduser('~')

    # version = None
    root = None
    bundle_root = None
    # pychron_src_root = None
    # doc_html_root = None
    icons = None
    splashes = None
    abouts = None
    sounds = None
    app_resources = None
    # _dir suffix ensures the path is checked for existence
    root_dir = root
    stable_root = None
    labspy_templates = None
    labspy_template_search_path = None
    icon_search_path = None
    resources = None
    #==============================================================================
    # #database
    #==============================================================================
    device_scan_root = device_scan_root = None
    device_scan_db = None

    co2laser_db_root = None
    co2laser_db = None

    diodelaser_db_root = None
    diodelaser_db = None

    isotope_db_root = None
    isotope_db = None
    #==============================================================================
    # root
    #==============================================================================
    scripts_dir = scripts_dir = None
    experiment_dir = None
    run_block_dir = None
    generic_experiment_dir = None
    backup_experiment_dir = None
    plugins_dir = None
    hidden_dir = None
    labspy_dir = None
    labspy_context_dir = None
    # users_file = None
    login_file = None
    preferences_dir = None
    comment_templates_dir = None
    plotter_options_dir = None
    test_dir = None
    custom_queries_dir = None
    template_dir = None
    log_dir = None
    #===========================================================================
    # scripts
    #===========================================================================
    procedures_dir = None
    measurement_dir = None
    post_measurement_dir = None
    extraction_dir = None
    post_equilibration_dir = None
    conditionals_dir = None
    hops_dir = None
    fits_dir = None
    #==============================================================================
    # setup
    #==============================================================================
    setup_dir = setup_dir = None
    device_dir = None
    spectrometer_dir = None
    backup_deflection_dir = None

    queue_conditionals_dir = None
    canvas2D_dir = None
    canvas3D_dir = None
    extraction_line_dir = None
    monitors_dir = None
    jog_dir = None
    pattern_dir = None
    incremental_heat_template_dir = None

    block_dir = None
    heating_schedule_dir = None
    map_dir = None
    user_points_dir = None
    irradiation_tray_maps_dir = None
    #==============================================================================
    # data
    #==============================================================================
    data_dir = None
    modeling_data_dir = None
    argus_data_dir = None
    positioning_error_dir = None
    snapshot_dir = None
    video_dir = None
    stage_visualizer_dir = None
    default_workspace_dir = None
    workspace_root_dir = None
    spectrometer_scans_dir = None
    processed_dir = None
    image_cache_dir = None
    default_cache = None
    loading_dir = None
    power_map_dir = None
    labbook_dir = None
    # vcs_dir = None
    # initialization_dir = None
    # device_creator_dir = None

    #==============================================================================
    # lovera exectuables
    #==============================================================================
    clovera_root = None

    #===========================================================================
    # files
    #===========================================================================
    backup_recovery_file = None
    last_experiment = None
    mftable = None
    deflection = None

    def set_search_paths(self, app_rec=None):
        self.app_resources = app_rec
        self.set_icon_search_path()
        self.set_sound_search_path()
        self.set_labspy_template_search_path()

    def set_icon_search_path(self):
        self.icon_search_path = [self.icons,
                                 self.app_resources]

    def set_sound_search_path(self):
        self.sound_search_path = [self.sounds,
                                  self.app_resources]

    def set_labspy_template_search_path(self):
        self.labspy_template_search_path = [self.labspy_templates,
                                            self.app_resources]

    def build(self, root):
        join = path.join
        # self.version = version
        if root.startswith('_'):
            root = join(path.expanduser('~'), 'Pychron{}'.format(root))

        if not path.isdir(root):
            os.mkdir(root)

        # self.root = root
        self.log_dir = join(root, 'logs')

        self.resources = join(path.dirname(path.dirname(__file__)), 'resources')
        self.icons = join(self.resources, 'icons')
        self.splashes = join(self.resources, 'splashes')
        self.labspy_templates = join(self.resources, 'labspy_templates')
        self.abouts = join(self.resources, 'abouts')
        self.sounds = join(self.resources, 'sounds')
        # self.bullets = join(self.resources, 'bullets')
        #        src_repo_name = 'pychron{}'.format(version)
        #        self.pychron_src_root = pychron_src_root = join('.', 'pychron.app', 'Contents', 'Resources')
        #        self.pychron_dev_src_root = join(HOME, 'Programming', 'mercurial',
        #                                             'pychron{}'.format(version),
        #                                             'resources'
        #                                            )

        self.root_dir = root
        # stable_root = join(HOME, 'Pychrondata')
        #==============================================================================
        # #database
        #==============================================================================
        #        db_path = '/usr/local/pychron
        # db_path = stable_root
        # self.device_scan_root = device_scan_root = join(db_path, 'device_scans')
        # self.device_scan_db = join(device_scan_root, 'device_scans.sqlite')

        # self.co2laser_db_root = join(db_path, 'co2laserdb')
        # self.co2laser_db = join(db_path, 'co2.sqlite')
        # self.uvlaser_db_root = join(db_path, 'uvlaserdb')
        # self.uvlaser_db = join(db_path, 'uv.sqlite')
        #
        # self.powermap_db_root = join(db_path, 'powermap')
        # self.powermap_db = join(db_path, 'powermap.sqlite')
        #
        # self.diodelaser_db_root = join(db_path, 'diodelaserdb')
        # self.diodelaser_db = join(db_path, 'diode.sqlite')
        # self.isotope_db_root = join(db_path, 'isotopedb')

        # ROOT = '/Users/ross/Sandbox/pychron_test_data/data'
        # self.isotope_db = join(ROOT, 'isotopedb.sqlite')
        #==============================================================================
        # root
        #==============================================================================
        self.scripts_dir = scripts_dir = join(root, 'scripts')
        self.procedures_dir = join(scripts_dir, 'procedures')
        self.measurement_dir = join(scripts_dir, 'measurement')
        self.post_measurement_dir = join(scripts_dir, 'post_measurement')
        self.extraction_dir = join(scripts_dir, 'extraction')
        self.post_equilibration_dir = join(scripts_dir, 'post_equilibration')
        self.conditionals_dir = join(scripts_dir, 'conditionals')
        self.hops_dir = join(self.measurement_dir, 'hops')
        self.fits_dir = join(self.measurement_dir, 'fits')

        self.experiment_dir = join(root, 'experiments')
        self.run_block_dir = join(self.experiment_dir, 'blocks')
        self.generic_experiment_dir = join(self.experiment_dir, 'generic')
        self.backup_experiment_dir = join(self.experiment_dir, 'backup')
        self.hidden_dir = join(root, '.hidden')
        # self.users_file = join(self.hidden_dir, 'users')
        self.login_file = join(self.hidden_dir, 'login')
        self.labspy_dir = join(self.hidden_dir, 'labspy')
        self.labspy_context_dir = join(self.labspy_dir, 'context')
        self.preferences_dir = join(root, 'preferences')
        self.plotter_options_dir = join(self.hidden_dir, 'plotter_options')
        self.comment_templates_dir = join(self.hidden_dir, 'comment_templates')
        # self.test_dir = join(root, 'testing')
        # self.custom_queries_dir = join(root, 'custom_queries')
        self.template_dir = join(root, 'templates')

        self.queue_conditionals_dir = join(root, 'queue_conditionals')
        #==============================================================================
        # setup
        #==============================================================================
        self.setup_dir = setup_dir = join(root, 'setupfiles')
        self.spectrometer_dir = join(setup_dir, 'spectrometer')
        self.backup_deflection_dir = join(self.spectrometer_dir, 'deflection_backup')
        self.device_dir = device_dir = join(setup_dir, 'devices')
        self.canvas2D_dir = join(setup_dir, 'canvas2D')
        # self.canvas3D_dir = join(setup_dir, 'canvas3D')
        self.extraction_line_dir = join(setup_dir, 'extractionline')
        self.monitors_dir = join(setup_dir, 'monitors')
        self.pattern_dir = join(setup_dir, 'patterns')
        self.incremental_heat_template_dir = join(setup_dir, 'incremental_heat_templates')

        self.block_dir = join(setup_dir, 'blocks')
        self.map_dir = map_dir = join(setup_dir, 'tray_maps')
        self.user_points_dir = join(map_dir, 'user_points')

        self.irradiation_tray_maps_dir = join(setup_dir, 'irradiation_tray_maps')
        #==============================================================================
        # data
        #==============================================================================
        self.data_dir = data_dir = join(root, 'data')
        self.spectrometer_scans_dir = join(data_dir, 'spectrometer_scans')
        self.modeling_data_dir = join(data_dir, 'modeling')
        self.argus_data_dir = join(data_dir, 'argusVI')
        self.positioning_error_dir = join(data_dir, 'positioning_error')
        self.snapshot_dir = join(data_dir, 'snapshots')
        self.video_dir = join(data_dir, 'videos')
        self.stage_visualizer_dir = join(data_dir, 'stage_visualizer')

        # self.arar_dir = join(data_dir, 'arar')

        self.isotope_dir = join(self.data_dir, 'isotopes')
        self.workspace_root_dir = join(self.data_dir, 'workspaces')
        self.default_workspace_dir = join(self.workspace_root_dir, 'collection')
        self.processed_dir = join(self.data_dir, 'processed')
        # initialization_dir = join(setup_dir, 'initializations')
        # device_creator_dir = join(device_dir, 'device_creator')
        self.image_cache_dir = join(self.data_dir, 'image_cache')
        self.default_cache = join(self.data_dir, 'cache')
        self.loading_dir = join(self.data_dir, 'loads')
        self.power_map_dir = join(self.data_dir, 'power_maps')
        self.labbook_dir = join(self.data_dir, 'labbook')
        # self.vcs_dir = join(self.data_dir, 'vcs')
        #==============================================================================
        # lovera exectuables
        #==============================================================================
        #        self.clovera_root = join(pychron_src_root, 'pychron', 'modeling', 'lovera', 'bin')


        #=======================================================================
        # files
        #=======================================================================
        self.backup_recovery_file = join(self.hidden_dir, 'backup_recovery')
        self.last_experiment = join(self.hidden_dir, 'last_experiment')
        self.mftable = join(self.spectrometer_dir, 'mftable.csv')
        self.deflection = join(self.spectrometer_dir, 'deflection.yaml')
        self.set_search_paths()


paths = Paths()
paths.build('_dev')


# def rec_make(pi):
#     if pi and not path.exists(pi):
#         try:
#             mkdir(pi)
#         except OSError:
#             rec_make(path.split(pi)[0])
#             mkdir(pi)

def r_mkdir(p):
    if p and not path.isdir(p):
        try:
            mkdir(p)
        except OSError:
            r_mkdir(path.dirname(p))
            mkdir(p)


def build_directories():
    #    global paths
    # verify paths
    #    import copy
    for l in dir(paths):
        if l.endswith('_dir'):
            r_mkdir(getattr(paths, l))

#============= EOF ==============================================
