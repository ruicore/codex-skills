<!-- PERSONAL_STYLE_DEFAULTS_START -->
## General coding style

- Use the repository's formatter, type checker, architecture, and compatibility requirements as the concrete rules for each project.
- Choose the smallest clear implementation. Introduce helpers for reuse, a complex boundary, or a meaningful concept; keep simple one-off expressions near their caller.
- Check external input where it enters the system, then work with the validated representation. Internal type hints alone are not runtime input validation.
- Keep the normal path easy to follow with guard clauses and shallow branching. Avoid reassignment and temporary values when they add no meaning.
- Keep names that explain domain meaning, units, or ownership; do not compress complicated logic just to reduce line count.
- Handle failures where there is a concrete recovery or error-translation policy. Catch specific errors around the relevant operation and use the language's cleanup mechanisms.
- Keep synchronous work synchronous unless the existing interface requires otherwise. Explain surprising constraints in comments rather than narrating obvious statements.
- Address demonstrated failure modes within the agreed scope. Discuss additional complexity for speculative edge cases before broadening the work.
<!-- PERSONAL_STYLE_DEFAULTS_END -->
