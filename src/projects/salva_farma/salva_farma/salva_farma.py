"""Welcome to Reflex!."""

import reflex as rx
from salva_farma import styles

# Import all the pages.
from salva_farma.pages import *

# Create the app and compile it.
app = rx.App(style=styles.base_style)
app.compile()
