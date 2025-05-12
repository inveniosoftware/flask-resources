from marshmallow import Schema


class WrapSchemaToPreserveContext(Schema):
    """Local wrapper for Schema to preserve context feature."""

    def __init__(self, *args, **kwargs):
        """Override constructor to squeeze in context"""
        context = kwargs.pop("context", {}) or {}
        super().__init__(*args, **kwargs)
        # it needs to be set here, otherwise the parent constructor would set
        # self.context to {}
        self.context = context

    def load(self, *args, **kwargs):
        """Override load to squeeze in context."""
        if context := kwargs.pop("context", None):
            self.context = context

        super().load(*args, **kwargs)
