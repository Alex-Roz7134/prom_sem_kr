from django import template
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

register = template.Library()

@register.filter(name='highlight_code')
def highlight_code(value):
    """
    Фильтр для подсветки синтаксиса Python
    """
    formatter = HtmlFormatter(style='monokai', linenos=True)  # используем более спокойный стиль 'monokai'
    return highlight(value, PythonLexer(), formatter)
