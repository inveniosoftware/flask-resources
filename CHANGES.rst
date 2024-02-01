..
    Copyright (C) 2020-2024 CERN.

    Flask-Resources is free software; you can redistribute it and/or
    modify it under the terms of the MIT License; see LICENSE file for more
    details.

Changes
=======

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
