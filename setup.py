from setuptools import find_packages, setup
import versioneer

setup(
    name='q2-SCNIC',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    license='BSD-3-Clause',
    packages=find_packages(),
    author="Michael Shaffer, Kumar Thurimella",
    author_email="CATHERINE.LOZUPONE@cuanschutz.edu",
    description=(
        "QIIME2 plugin for using SCNIC."),
    url="https://github.com/lozuponelab/q2-SCNIC",
    package_data={
        'q2_SCNIC': ['citations.bib']
    },
    entry_points={
        'qiime2.plugins':
        ['q2-SCNIC=q2_SCNIC.plugin_setup:plugin']
    }
)
