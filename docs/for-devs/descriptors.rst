Plugin Descriptors
==================

.. autoclass:: peakrdl.plugins.exporter.ExporterSubcommandPlugin
    :members: short_desc, long_desc, generates_output_file, udp_definitions,
        cfg_schema, cfg, add_exporter_arguments, do_export


.. autoclass:: peakrdl.plugins.importer.ImporterPlugin
    :members: file_extensions, cfg_schema, cfg,
        is_compatible, add_importer_arguments, do_import
