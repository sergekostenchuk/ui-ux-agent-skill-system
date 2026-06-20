# Form Patterns

## Required States

- Pristine.
- Dirty.
- Validating.
- Field error.
- Form error.
- Disabled.
- Submitting.
- Success.

## Rules

- Put validation messages near the field they explain.
- Keep destructive actions visually distinct.
- Preserve user input after recoverable failures.
- Avoid disabled controls with no explanation when the user can reasonably expect action.
- Use inline progress only where it does not shift layout.

## Verification

- Keyboard through every input.
- Submit invalid data and inspect errors.
- Submit valid data and inspect success/recovery state.
- Check mobile touch targets and label wrapping.
