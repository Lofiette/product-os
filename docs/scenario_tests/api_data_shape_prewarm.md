# api_data_shape_prewarm

## Purpose
Validate frontend-facing API/data contract prewarm without backend deep dive.

## Expected behavior
- Start with path scan if needed.
- Read only approved shared API/client/proxy/type files.
- Extract UI/product implications: errors, statuses, filters, tokens/auth, write-only secret fields, open-ended backend strings.
- Leave endpoint/mutation/cache/backend validation task-driven unless task requires it.

## Must not
- Read all backend/API files.
- Convert API/Data Shape into backend documentation.
- Implement code.
