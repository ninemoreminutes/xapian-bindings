#!/usr/bin/env python

# Python
import os
import shutil
import subprocess
import sys
import tarfile
from distutils.spawn import find_executable

# Setuptools
from setuptools import Command, setup
import setuptools.command.install as orig_install

# Wheel
import wheel.bdist_wheel as orig_bdist_wheel


class XapianConfigCommand(Command):

    description = 'xapian config'

    user_options = [
        ('build-temp=', 't',
         "directory to put temporary build by-products"),
        ('xapian-config=', None,
         'path to xapian-config command (searches path by default)'),
        ('xapian-version=', None,
         'version of xapian-bindings to build (uses xapian-config --version by default)'),
    ]

    def initialize_options(self):
        self.build_temp = None
        self.xapian_config = None
        self.xapian_version = None

    def finalize_options(self):
        self.set_undefined_options(
            'build',
            ('build_temp', 'build_temp'),
        )
        if self.xapian_config is None:
            self.xapian_config = 'xapian-config'

    def run(self):
        xapian_config = find_executable(self.xapian_config)
        if not xapian_config:
            raise RuntimeError('{0} not found'.format(self.xapian_config))
        print(xapian_config)
        xc_version_output = subprocess.check_output([xapian_config, '--version'])
        xc_version = xc_version_output.strip().rsplit()[-1].decode()
        if self.xapian_version is None:
            self.xapian_version = xc_version
        elif self.xapian_version != xc_version:
            print('warning: {0} != {1}'.format(self.xapian_version, xc_version))
            self.xapian_version = xc_version
        print(self.xapian_version)


class XapianDownloadCommand(Command):

    description = 'xapian download'

    user_options = [
        ('build-temp=', 't',
         "directory to put temporary build by-products"),
        ('xapian-version=', None,
         'version of xapian-bindings to download (uses xapian-config --version by default)'),
        ('xapian-url=', None,
         'custom url for xapian bindings'),
        ('xapian-archive=', None,
         'custom path to archive file for xapian bindings'),
    ]

    def initialize_options(self):
        self.build_temp = None
        self.xapian_version = None
        self.xapian_url = None
        self.xapian_archive = None

    def finalize_options(self):
        self.set_undefined_options(
            'xapian_config',
            ('build_temp', 'build_temp'),
            ('xapian_version', 'xapian_version'),
        )

    def run(self):
        if not self.xapian_url:
            if not self.xapian_version:
                self.run_command('xapian_config')
                xapian_config_cmd = self.get_finalized_command('xapian_config')
                self.xapian_version = xapian_config_cmd.xapian_version
            if not self.xapian_url:
                self.xapian_url = 'https://oligarchy.co.uk/xapian/{0}/xapian-bindings-{0}.tar.xz'.format(self.xapian_version)
        print(self.xapian_url)
        if not self.xapian_archive:
            self.xapian_archive = os.path.join(self.build_temp, self.xapian_url.split('/')[-1])
        if not os.path.exists(os.path.dirname(self.xapian_archive)):
            os.makedirs(os.path.dirname(self.xapian_archive))
        import requests  # noqa
        response = requests.get(self.xapian_url, stream=True)
        print(response.headers)
        content_length = response.headers.get('Content-Length', None)
        if os.path.exists(self.xapian_archive):
            xb_size = os.path.getsize(self.xapian_archive)
        else:
            xb_size = 0
        if xb_size == 0 or xb_size != content_length:
            # FIXME: Check PGP signature!
            with response.raw as xb_dl:
                with open(self.xapian_archive, 'wb') as xb_archive:
                    shutil.copyfileobj(xb_dl, xb_archive)


class XapianExtractCommand(Command):

    description = 'xapian extract'

    user_options = [
        ('build-temp=', 't',
         "directory to put temporary build by-products"),
        ('xapian-archive=', None,
         'path to xapian bindings archive'),
    ]

    def initialize_options(self):
        self.build_temp = None
        self.xapian_archive = None
        self.xapian_src_dir = None

    def finalize_options(self):
        self.set_undefined_options(
            'xapian_download',
            ('build_temp', 'build_temp'),
            ('xapian_archive', 'xapian_archive'),
        )

    def run(self):
        if not self.xapian_archive:
            self.run_command('xapian_download')
            xapian_download_cmd = self.get_finalized_command('xapian_download')
            self.xapian_archive = xapian_download_cmd.xapian_archive

        tf_root_dirs = set()
        with tarfile.open(self.xapian_archive) as tf:
            for name in tf.getnames():
                tf_root_dirs.add(name.split('/')[0])
            tf.extractall(self.build_temp)
        print(tf_root_dirs)
        self.xapian_src_dir = os.path.join(self.build_temp, list(tf_root_dirs)[0])


class XapianBuildCommand(Command):

    description = 'xapian build'

    user_options = [
        ('xapian-config=', None,
         'path to xapian config'),
        ('xapian-src-dir=', None,
         'path to xapian bindings archive'),
        ('xapian-prefix=', None,
         'path prefix where xapian bindings will be installed'),
    ]

    def initialize_options(self):
        self.xapian_config = None
        self.xapian_src_dir = None
        self.xapian_prefix = None

    def finalize_options(self):
        self.set_undefined_options(
            'xapian_config',
            ('xapian_config', 'xapian_config'),
        )
        self.set_undefined_options(
            'xapian_extract',
            ('xapian_src_dir', 'xapian_src_dir'),
        )
        self.set_undefined_options(
            'install',
            ('root', 'xapian_prefix'),
        )

    def run(self):
        if not self.xapian_config:
            self.run_command('xapian_config')
            xapian_config_cmd = self.get_finalized_command('xapian_config')
            self.xapian_config = xapian_config_cmd.xapian_config
        if not self.xapian_src_dir:
            self.run_command('xapian_extract')
            xapian_extract_cmd = self.get_finalized_command('xapian_extract')
            self.xapian_src_dir = xapian_extract_cmd.xapian_src_dir
        if not self.xapian_prefix:
            install_cmd = self.get_finalized_command('install')
            self.xapian_prefix = install_cmd.root or sys.prefix
        self.xapian_prefix = os.path.normpath(os.path.abspath(self.xapian_prefix))

        xb_build_env = dict(os.environ.items())
        xb_build_env['XAPIAN_CONFIG'] = self.xapian_config
        xb_build_env['PYTHON3'] = os.path.normpath(sys.executable)
        xb_build_env['PYTHON3_LIB'] = self.xapian_prefix
        xb_build_env['PYTHONPATH'] = os.path.pathsep.join(sys.path)

        subprocess.check_call(['./configure', '--with-python3', '--prefix={}'.format(self.xapian_prefix)], cwd=self.xapian_src_dir, env=xb_build_env)

        subprocess.check_call(['make', 'clean', 'all'], cwd=self.xapian_src_dir, env=xb_build_env)


class XapianInstallCommand(Command):

    description = 'xapian install'

    user_options = [
        ('xapian-config=', None,
         'path to xapian config'),
        ('xapian-src-dir=', None,
         'path to xapian bindings archive'),
        ('xapian-prefix=', None,
         'path prefix where xapian bindings will be installed'),
    ]

    def initialize_options(self):
        self.xapian_config = None
        self.xapian_src_dir = None
        self.xapian_prefix = None

    def finalize_options(self):
        self.set_undefined_options(
            'xapian_build',
            ('xapian_config', 'xapian_config'),
            ('xapian_src_dir', 'xapian_src_dir'),
            ('xapian_prefix', 'xapian_prefix'),
        )

    def run(self):
        if not self.xapian_config or not self.xapian_src_dir or not self.xapian_prefix:
            self.run_command('xapian_build')
            xapian_build_cmd = self.get_finalized_command('xapian_build')
            if not self.xapian_config:
                self.xapian_config = xapian_build_cmd.xapian_config
            if not self.xapian_src_dir:
                self.xapian_src_dir = xapian_build_cmd.xapian_src_dir
            if not self.xapian_prefix:
                self.xapian_prefix = xapian_build_cmd.xapian_prefix

        xb_build_env = dict(os.environ.items())
        xb_build_env['XAPIAN_CONFIG'] = self.xapian_config
        xb_build_env['PYTHON3'] = os.path.normpath(sys.executable)
        xb_build_env['PYTHON3_LIB'] = self.xapian_prefix
        xb_build_env['PYTHONPATH'] = os.path.pathsep.join(sys.path)
        xb_build_env['PYTHONDONTWRITEBYTECODE'] = '0'

        subprocess.check_call(['make', 'install'], cwd=self.xapian_src_dir, env=xb_build_env)

        share_path = os.path.join(self.xapian_prefix, 'share')
        if os.path.exists(share_path):
            shutil.rmtree(share_path)


class BaseTwineCommand(Command):

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        for sub_cmd in self.get_sub_commands():
            self.run_command(sub_cmd)
            self.get_finalized_command(sub_cmd)
        dist_files = [df[2] for df in self.distribution.dist_files]
        self.spawn(['twine', self.twine_subcommand] + dist_files)

    sub_commands = [
        ('sdist', lambda self: True),
    ]


class TwineCheckCommand(BaseTwineCommand):

    description = 'Check distribution files with twine'
    twine_subcommand = 'check'


class TwineUploadCommand(BaseTwineCommand):

    description = 'Upload distribution files with twine'
    twine_subcommand = 'upload'


class UnsupportedCommand(Command):

    description = 'This command is not supported'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        sys.exit('This command is not supported!')


class InstallCommand(orig_install.install):

    def do_egg_install(self):
        sys.exit('Egg install is not supported!')


InstallCommand.sub_commands = orig_install.install.sub_commands + [
    ('xapian_install', lambda self: True),
]


class BdistWheelCommand(orig_bdist_wheel.bdist_wheel):

    def finalize_options(self):
        if not self.build_number:
            self.run_command('xapian_config')
            xapian_config_cmd = self.get_finalized_command('xapian_config')
            self.build_number = xapian_config_cmd.xapian_version
        orig_bdist_wheel.bdist_wheel.finalize_options(self)
        self.root_is_pure = False


setup(
    cmdclass={
        'xapian_config': XapianConfigCommand,
        'xapian_download': XapianDownloadCommand,
        'xapian_extract': XapianExtractCommand,
        'xapian_build': XapianBuildCommand,
        'xapian_install': XapianInstallCommand,
        'install': InstallCommand,
        'bdist_wheel': BdistWheelCommand,
        'twine_check': TwineCheckCommand,
        'twine_upload': TwineUploadCommand,
        'unsupported': UnsupportedCommand,
        'bdist_egg': UnsupportedCommand,
        'develop': UnsupportedCommand,
        'easy_install': UnsupportedCommand,
        'upload_docs': UnsupportedCommand,
    },
)
