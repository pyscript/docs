"""
Pirate translator - translate English to Pirate speak.
"""
import arrr
from pyscript import web, when


@when("click", "#translate-button")
def translate_english(event):
    """
    Translate English text to Pirate speak.
    """
    input_text = web.page["english"]
    english = input_text.value
    output_div = web.page["output"]
    output_div.innerText = arrr.translate(english)