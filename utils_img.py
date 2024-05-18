from PIL import Image, ImageDraw, ImageFont, ImageCms
from io import BytesIO
import pandas as pd

def add_sl_to_image(image_path, text, font_size=20, text_position=(10, 10), text_color=(0, 0, 0)):
    # Open the image
    image = Image.open(image_path)
    if 'icc_profile' in image.info:
        icc_profile = image.info['icc_profile']
        # Convert image to sRGB if it's not already in sRGB
        srgb_profile = ImageCms.createProfile("sRGB")
        input_profile = ImageCms.ImageCmsProfile(BytesIO(icc_profile))
        image = ImageCms.profileToProfile(image, input_profile, srgb_profile, outputMode='RGB')
    
    # Ensure image is loaded properly
    image.load()
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.truetype("MyriadPro-Bold.ttf", font_size)

    # Get bounding box of text
    text_bbox = draw.textbbox(text_position, text, font=font)

    # Calculate centered position
    text_width = text_bbox[2] - text_bbox[0]
    text_position = (text_position[0] - text_width // 2, text_position[1])
    
    # Add text onto the image
    draw.text(text_position, text, fill=text_color, font=font)
    
    # Save the modified image
    return image

def add_title_to_image(image, text, font_size=20, text_position=(10, 10), text_color=(0, 0, 0)):
    # Open the image
    draw = ImageDraw.Draw(image)
    
    # Load a font
    font = ImageFont.truetype("MyriadPro-Semibold.ttf", font_size)
    
    # Add text onto the image
    draw.text(text_position, text, fill=text_color, font=font)
    
    # Save the modified image
    return image

def add_overlay_image(background_image, overlay_image_path, resize, overlay_position=(0, 0), rotate_angle = 0):
    # Open the overlay image
    overlay_image = Image.open(overlay_image_path)

    if overlay_image.mode != 'RGBA':
        overlay_image = overlay_image.convert('RGBA')

    if resize is not None:
        overlay_image = overlay_image.resize(resize)

    if rotate_angle != 0:
        overlay_image = overlay_image.rotate(rotate_angle, resample=Image.BICUBIC,expand=1)
    
    mask_image = overlay_image.split()[3]
    
    background_image.paste(overlay_image,overlay_position,mask_image)

    # Save the modified image
    return background_image
# Function to split text into multiple lines
def split_text(text, draw, font, max_width):
    lines = []
    words = text.split()
    while words:
        line = ''
        while words and draw.textlength(line + words[0], font=font) <= max_width:
            line = line + (words.pop(0) + ' ')
        lines.append(line.strip())
    return lines

def draw_textbox(image,text,box_position,box_size,font_size=20,text_color=(0,0,0),line_space = 50):
    # Load Font
    font = ImageFont.truetype("MyriadPro-Regular.ttf",size=font_size)
    # create a separate image for the text box
    text_layer = Image.new("RGBA", image.size, (255, 255, 255, 0))
    text_draw = ImageDraw.Draw(text_layer)
    # Split the text to fit within the box size
    lines = split_text(text=text,draw=text_draw,font=font,max_width=box_size[0])
    # Draw each line of text within box
    y_offset = box_position[1]
    for line in lines:
        text_draw.text((box_position[0],y_offset),line,font=font,fill=text_color)
        y_offset += line_space
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    combined = Image.alpha_composite(image,text_layer)
    return combined

# # Example usage Case1:
# filepath = "C:\\Users\\ankus\\Documents\\G-Map\\6. Automation\\Whispers\\Input_Data\\Whispers_Data.csv"
# df_whispers = pd.read_csv(filepath)
# image_path = "WhispersTemplate.jpg"
# text = str(df_whispers['SlNo'][0])
# modified_image = add_sl_to_image(image_path,text,font_size=250,text_position=(204,150),text_color=(227,29,76))
# # modified_image.show()
# title = df_whispers['Title'][0]
# title_image = add_title_to_image(modified_image,text=title,font_size=105,text_position=(510,630),text_color=(227,29,76))
# # title_image.show()

# overlay_image_path = f"{text}.jpg"
# overlay_image = add_overlay_image(title_image,overlay_image_path,resize = (1700,990), overlay_position=(530,820))
# # overlay_image.show()

# # Adding a Paragraph
# text = df_whispers['Content'][0]

# textbox_image = draw_textbox(image=overlay_image,text=text,box_position=(475,2015),box_size=(1850,2000),font_size=75,text_color=(32,27,83),line_space=105)
# textbox_image.show()

# # Example usage Case2:
# filepath = "C:\\Users\\ankus\\Documents\\G-Map\\6. Automation\\Whispers\\Input_Data\\Whispers_Data.csv"
# df_whispers = pd.read_csv(filepath)
# image_path = "WhispersTempBenefits.jpg"
# text = str(df_whispers['SlNo'][0])
# modified_image = add_sl_to_image(image_path,text,font_size=250,text_position=(204,150),text_color=(227,29,76))
# # modified_image.show()
# title = df_whispers['Title'][0]
# title_image = add_title_to_image(modified_image,text=title,font_size=105,text_position=(510,830),text_color=(32,27,83))
# # title_image.show()

# overlay_image_path = f"{text}.jpg"
# overlay_image = add_overlay_image(title_image,overlay_image_path,resize = (1700,990), overlay_position=(530,1030))
# # overlay_image.show()

# # # Adding a Paragraph
# text = df_whispers['Content'][0]

# textbox_image = draw_textbox(image=overlay_image,text=text,box_position=(475,2215),box_size=(1850,2000),font_size=75,text_color=(32,27,83),line_space=105)
# textbox_image.show()