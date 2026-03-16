"""Module for printing a greeting message."""


def greet(name: str = "World") -> str:
    """Return a greeting string for the given name.

    Args:
        name: The name to greet. Defaults to "World".

    Returns:
        A formatted greeting string.
    """
    return f"Hello, {name}!"


def main() -> None:
    """Entry point: print the greeting to stdout."""
    print(greet())


if __name__ == "__main__":
    main()
