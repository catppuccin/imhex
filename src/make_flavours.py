from dataclasses import fields
from pathlib import Path
from string import Template

from catppuccin import Flavour

OUT_DIR = Path("build")
OUT_DIR.mkdir(exist_ok=True)
TEMPLATE_STR = Path("src/flavour-template.json").read_text()

def palette():
    return {
        flavour_method.__name__: {
            field.name: f"#{getattr(flavour_method(), field.name).hex}"
            for field in fields(flavour_method())
        } for flavour_method in [Flavour.latte, Flavour.frappe, Flavour.macchiato, Flavour.mocha]
    }

def generate_color_with_transparency(color_hex: str) -> str:
    # Extract RGB values from color_hex
    r = int(color_hex[1:3], 16)
    g = int(color_hex[3:5], 16)
    b = int(color_hex[5:7], 16)
    
    # Generate the RGBA color string
    rgba = f"rgba({r}, {g}, {b}, 0.5)"  # Change the alpha value (0.5) as desired
    
    return rgba


if __name__ == "__main__":
    template = Template(TEMPLATE_STR)
    for flavour, colours in palette().items():
        # Determine the custom values based on the flavor
        theme_base = "Light" if flavour.lower() == "latte" else "Dark"
        image_postfix = f"_{theme_base.lower()}"
        theme_name = f"Catppuccin {flavour.capitalize()}"
        transparent = "#00000000"
        plot_background = f"{colours['blue']}21"

        # Generate color values with transparency
        for color_name, color_value in colours.items():
            if color_name.endswith("7f"):
                # Skip colors that already have transparency
                continue
            if color_value.startswith("#"):
                # Generate color with transparency
                color_with_transparency = generate_color_with_transparency(color_value)
                colours[color_name + "7f"] = color_with_transparency

        # Add the custom values to the colours dictionary
        colours["theme_base"] = theme_base
        colours["image_postfix"] = image_postfix
        colours["theme_name"] = theme_name
        colours["transparent"] = transparent
        colours["plot_background"] = plot_background

        # Substitute the template with the updated colours dictionary
        substituted_template = template.substitute(colours)

        # Write the substituted template to the output file
        open(OUT_DIR / f"catppuccin-{flavour}.json", 'w').write(substituted_template)