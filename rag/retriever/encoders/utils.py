def safe_text_slice(
    text: str | list[str], start: int, length: int, mode: str = "words"
) -> tuple[str | list[str], int, int]:
    """
    Safely slices a piece of text or a list of tokens without cutting words or tokens in half.

    :param text: The input text to slice. Can be either a string (in ``mode='words'``) or a list of tokens (in ``mode='tokens'``).
    :param start: The starting index for the slice.
    :param length: The maximum length of the slice.
    :param mode: The mode of operation. Use ``'words'`` for slicing a string or ``'tokens'`` for slicing a list of tokens.
    :returns: A tuple containing the sliced text or token list, start index, and end index.
    :raises ValueError: If the mode is invalid or the type of ``text`` does not match the selected ``mode``.
    """
    if mode == "words" and isinstance(text, str):
        # Строковый режим для обрезки слов
        if start >= len(text):
            return "", 0, 0

        if start > 0 and text[start - 1].isalnum():
            start = text.rfind(" ", 0, start) + 1

        end = start + length
        if end < len(text) and text[end].isalnum():
            end = text.find(" ", end)
            if end == -1:
                end = len(text)

        return text[start:end].strip(), start, end

    elif mode == "tokens" and isinstance(text, list):
        # Токенизированный режим для списка
        if start >= len(text):
            return []

        if start > 0 and not text[start].startswith("▁"):
            while start > 0 and not text[start].startswith("▁"):
                start -= 1

        end = start + length
        if end < len(text) and not text[end].startswith("▁"):
            while end > start and end < len(text) and not text[end].startswith("▁"):
                end -= 1

        return text[start:end], start, end

    else:
        raise ValueError(
            "Invalid mode or text type. Use 'words' for string text or 'tokens' for list of tokens."
        )
