"""Public workflow API. The fixed-rule demo is in baseline.py."""
from .context import ContextBundle, ContextSpec, capture_context, local_changes, normalize_changes
from .personas import finalize_distillation, import_history, prepare_distillation, validate_profile
from .workflow import finalize_review, markdown_report, prepare_review
