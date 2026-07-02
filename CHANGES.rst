..
    SPDX-FileCopyrightText: 2020-2024 CERN.
    SPDX-FileCopyrightText: 2026 Graz University of Technology.
    SPDX-FileCopyrightText: 2026 TU Wien.
    SPDX-License-Identifier: MIT

Changes
=======

Version v1.3.1 (released 2026-07-02)

- chore(setup): migrate build backend from setuptools to hatchling
- chore(format): reformat with black
- chore(licenses): update license headers to use SPDX

Version v1.3.0 (released 2026-01-27)

- refactor: move object_schema_cls to constructor
- refactor(schema): make object_key class property
- setup: change to reusable workflows
- fix: setuptools require underscores instead of dashes
- tests: create tests for CSVSerializer

Version 1.2.0 (released 2024-02-01)

- Add CSV serializer
- Added links and sortby options to list schemas

Version 1.1.0 (released 2023-04-17)

- Serializers: add marshmallow schema processors

Version 1.0.0 (released 2023-03-09)

- Remove MarshmallowJSONSerializer (deprecated).
- Remove XMLSerializer in favor of SimpleSerializer with encoder function.
- Remove SerializerMixin in favor of BaseSerializer interface.
- Replace flask.JSONEncoder by json.JSONEncoder.

Version 0.9.1 (released 2023-02-24)

- Fix bug on XML object and object list serialization formatting.

Version 0.9.0 (released 2023-02-24)

- Add deprecation warning to MarshmallowJSONSerializer.
- Add support for XML serialization formatting.

Version 0.1.0 (released TBD)

- Initial public release.
