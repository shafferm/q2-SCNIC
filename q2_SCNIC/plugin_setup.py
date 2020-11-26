import importlib

from qiime2.plugin import (Str, Plugin, Choices, Float, Range, Bool, Citations, Int)
from q2_types.feature_table import FeatureTable, Frequency

from q2_SCNIC._type import Network, PairwiseFeatureData, ModuleMembership
from q2_SCNIC._format import GraphModelingLanguageFormat, GraphModelingLanguageDirectoryFormat, PairwiseFeatureDataFormat, \
                     PairwiseFeatureDataDirectoryFormat, ModuleMembershipTSVFormat, ModuleMembershipTSVDirectoryFormat
from q2_SCNIC._SCNIC_methods import sparcc_filter, calculate_correlations, build_correlation_network_r, \
                            build_correlation_network_p, make_modules_on_correlations

import q2_SCNIC

citations = Citations.load('citations.bib', package='q2_SCNIC')

plugin = Plugin(
    name='SCNIC',
    version=q2_SCNIC.__version__,
    website="https://github.com/lozuponelab/q2-SCNIC",
    package='q2_SCNIC',
    description=(
        'This QIIME 2 plugin allows for use of the SCNIC methods '
        'to build correlation networks as well as detect and '
        'summarize modules of highy intercorrelated features'),
    short_description='Plugin for SCNIC usage.',
    citations=[citations['SciPyProceedings_11']]
)

plugin.register_semantic_types(Network)
plugin.register_semantic_types(PairwiseFeatureData)
plugin.register_semantic_types(ModuleMembership)

plugin.register_formats(GraphModelingLanguageFormat)
plugin.register_formats(GraphModelingLanguageDirectoryFormat)
plugin.register_formats(PairwiseFeatureDataFormat)
plugin.register_formats(PairwiseFeatureDataDirectoryFormat)
plugin.register_formats(ModuleMembershipTSVFormat)
plugin.register_formats(ModuleMembershipTSVDirectoryFormat)

plugin.register_semantic_type_to_format(Network, artifact_format=GraphModelingLanguageDirectoryFormat)
plugin.register_semantic_type_to_format(PairwiseFeatureData, artifact_format=PairwiseFeatureDataDirectoryFormat)
plugin.register_semantic_type_to_format(ModuleMembership, artifact_format=ModuleMembershipTSVDirectoryFormat)

plugin.methods.register_function(
    function=sparcc_filter,
    inputs={'table': FeatureTable[Frequency]},
    parameters={},
    outputs=[('table_filtered', FeatureTable[Frequency])],
    input_descriptions={'table': (
        'Table to be filtered for use in correlational analyses.')},
    output_descriptions={'table_filtered': 'The filtered table.'},
    name='Filter a table based on recommended parameters from Friedman et al. 2012',
    description=(
        'Filter a feature table based on recommendations from Friedman et al. 2012.'
        'Samples with a count of less than 500 and features with mean abundance of '
        '<2 are removed.'
    ),
)

plugin.methods.register_function(
    function=calculate_correlations,
    inputs={'table': FeatureTable[Frequency]},  # TODO: Generalize, don't require frequency
    parameters={'method': Str % Choices(['kendall', 'pearson', 'spearman', 'sparcc']),
                'p_adjustment_method': Str, 'n_procs': Int, 'sparcc_p': Bool, 'bootstraps': Int},
    outputs=[('correlation_table', PairwiseFeatureData)],
    input_descriptions={'table': (
        'Normalized and filtered feature table to use for microbial interdependence test.')},
    parameter_descriptions={
        'method': 'The correlation test to be applied.',
        'p_adjustment_method': 'The method for p-value adjustment to be applied. '
                               'This can be selected from the list of methods in '
                               'statsmodels multipletests.',
        'n_procs': 'Number of processors to use in correlation analysis',
        'sparcc_p': 'Calculate sparCC p-value using permutation test.',
        'bootstraps': 'Give number of bootstraps for sparCC p-value calculation. Will dramatically increase runtime'
                      'based on number of bootstraps.'
    },
    output_descriptions={'correlation_table': 'The resulting table of pairwise correlations with R and p-value.'},
    name='Build pairwise correlations between observations',
    description=(
        'Build pairwise correlations between all observations in feature table'
    ),
    citations=[citations['Friedman2012'], citations['Watts2018']]
)

plugin.methods.register_function(
    function=build_correlation_network_r,
    inputs={'correlation_table': PairwiseFeatureData},
    parameters={'min_val': Float % Range(0, 1, inclusive_end=True),
                'cooccur': Bool},
    outputs=[('correlation_network', Network)],
    input_descriptions={'correlation_table': (
        'Pairwise feature data table of correlations with r value.')},
    parameter_descriptions={
        'min_val': 'The minimum r value to say an edge should exist.',
        'cooccur': 'Whether or not to constrain the network to only positive edges.'
    },
    output_descriptions={'correlation_network': 'The resulting network.'},
    name='Build a correlation network based on an r value cutoff',
    description=(
        'Build a correlation network where nodes are features and edges '
        'are correlations are stronger than the provided min_val.'
    ),
)

plugin.methods.register_function(
    function=build_correlation_network_p,
    inputs={'correlation_table': PairwiseFeatureData},
    parameters={'max_val': Float % Range(0, 1, inclusive_end=True)},
    outputs=[('correlation_network', Network)],
    input_descriptions={'correlation_table': (
        'Pairwise feature data table of correlations with .')},
    parameter_descriptions={
        'max_val': 'The maximum p value to say an edge should exist.'
    },
    output_descriptions={'correlation_network': 'The resulting network.'},
    name='Build a correlation network based on a p value cutoff',
    description=(
        'Build a correlation network where nodes are features and edges '
        'are correlations with a p-value (or adjusted p-value) less than '
        'the max_val.'
    ),
)

# TODO: expose min_p based module making
plugin.methods.register_function(
    function=make_modules_on_correlations,
    inputs={'correlation_table': PairwiseFeatureData,
            'feature_table': FeatureTable[Frequency]},
    parameters={'min_r': Float % Range(0, 1, inclusive_end=True)},
    outputs=[('collapsed_table', FeatureTable[Frequency]),
             ('correlation_network', Network),
             ('module_membership', ModuleMembership)],
    input_descriptions={
        'correlation_table': 'Pairwise feature data table of correlations.',
        'feature_table': 'Feature table used to calculated correlations'
    },
    parameter_descriptions={'min_r': 'Minimum R value for creating an edge.'},
    output_descriptions={
        'collapsed_table': 'Feature table with module members collapsed into single observations.',
        'correlation_network': 'Network annotated with module membership and edges where correlation'
                               'was stronger than min_r',
        'module_membership': 'Feature metadata with module membership'
    },
    name='Find modules via the SCNIC method',
    description=(
        'Use the SCNIC method to find modules in a correlation network based '
        'on a minimum R value. A collapsed table and an annotated network are output.'
    ),
)

importlib.import_module('q2_SCNIC._transformer')
