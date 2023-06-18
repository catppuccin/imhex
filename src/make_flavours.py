from dataclasses import fields
from pathlib import Path
from string import Template
from PIL import ImageColor

from catppuccin import Flavour

OUT_DIR = Path("build")
OUT_DIR.mkdir(exist_ok=True)
TEMPLATE_STR = Path("src/flavour-template.json").read_text()
TRANSPARENCY = "7f"

def palette():
    return {
        flavour_method.__name__: {
            field.name: f"#{getattr(flavour_method(), field.name).hex}"
            for field in fields(flavour_method())
        } for flavour_method in [Flavour.latte, Flavour.frappe, Flavour.macchiato, Flavour.mocha]
    }

def generate_colour_with_transparency(colour_value, transparency):
    rgba_value = ImageColor.getrgb(colour_value)
    rgba_value_with_transparency = rgba_value[:3] + (transparency,)
    return f"#{''.join(format(c, '02x') for c in rgba_value_with_transparency)}"

if __name__ == "__main__":
    template = Template(TEMPLATE_STR)
    for flavour, colours in palette().items():
        # Determine the custom values based on the flavour
        theme_base = "Light" if flavour.lower() == "latte" else "Dark"
        image_postfix = f"_{theme_base.lower()}"
        theme_name = f"Catppuccin {flavour.capitalize()}"
        transparent = "#00000000"
        plot_background = f"{colours['blue']}21"

        # Create a new dictionary to store transparent colours
        transparent_colours = dict(colours)

        # Generate colour values with transparency
        for colour_name, colour_value in colours.items():
            if colour_name.endswith(TRANSPARENCY):
                # Skip colours that already have transparency
                continue
            if colour_value.startswith("#"):
                # Generate colour with transparency
                colour_with_transparency = generate_colour_with_transparency(colour_value, TRANSPARENCY)
                transparent_colours[colour_name + TRANSPARENCY] = colour_with_transparency

        # Add the custom values to the transparent_colours dictionary
        transparent_colours["theme_base"] = theme_base
        transparent_colours["image_postfix"] = image_postfix
        transparent_colours["theme_name"] = theme_name
        transparent_colours["transparent"] = transparent
        transparent_colours["plot_background"] = plot_background

        # Substitute the template with the updated transparent_colours dictionary
        substituted_template = template.substitute(transparent_colours)

        # Write the substituted template to the output file
        open(OUT_DIR / f"catppuccin-{flavour}.json", 'w').write(substituted_template)
