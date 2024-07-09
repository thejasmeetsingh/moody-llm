import re


def escape_html(text):
    """Escape HTML special characters in the given text."""
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&#x27;",
        ">": "&gt;",
        "<": "&lt;",
    }
    return "".join(html_escape_table.get(c, c) for c in text)


def markdown_to_html(markdown):
    # Escape HTML special characters
    markdown = escape_html(markdown)

    # Replace single star (*) with <i> tags
    markdown = re.sub(r'\*(.*?)\*', r'<b><em>\1</em></b>', markdown)

    # Replace double star (**) with <b> tags
    markdown = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown)

    # Replace triple backtick with language (```lang) with <pre><code class="lang"> tags
    markdown = re.sub(r'```(\w+)\n(.*?)```',
                      r'<pre><code class="language-\1">\2</code></pre>', markdown, flags=re.DOTALL)

    # Replace triple backtick (```) with <pre><code> tags
    markdown = re.sub(r'```([^`]*)```',
                      r'<pre><code>\1</code></pre>', markdown)

    # Replace single backtick (`) with <code> tags
    markdown = re.sub(r'`([^`]*)`', r'<code>\1</code>', markdown)

    # # Replace new line characters with <br> tags
    # markdown = markdown.replace('\n', '<br>')
    # Replace new line characters with <br> tags, but not inside <pre><code> blocks
    parts = re.split(r'(<pre><code.*?>.*?</code></pre>)',
                     markdown, flags=re.DOTALL)

    for i, part in enumerate(parts):
        if not part.startswith('<pre><code'):
            parts[i] = part.replace('\n', '<br>')
    markdown = ''.join(parts)

    return markdown
