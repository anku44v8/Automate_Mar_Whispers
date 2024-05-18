# Import Libraries
import os
import pandas as pd
import numpy as np
from PIL import ImageFont, ImageDraw, Image
from utils_img import add_sl_to_image,add_title_to_image,add_overlay_image,split_text,draw_textbox

# FilePaths
imagePath = "C:\\Users\\ankus\\Documents\\G-Map\\6. Automation\\Whispers\\Input_Data\\Images"
templatePath = "C:\\Users\\ankus\\Documents\\G-Map\\6. Automation\\Whispers\\Input_Data"
dataPath = templatePath
outputPath = "C:\\Users\\ankus\\Documents\\G-Map\\6. Automation\\Whispers\\Output"
FileName = "Whispers_Data.csv"

# Create directory for output if not already present
if not os.path.exists(outputPath):
    os.makedirs(outputPath)

# Read Names
dataPath = f"{dataPath}\\{FileName}"
df_inputData = pd.read_csv(filepath_or_buffer=dataPath)

nrows = df_inputData.shape[0]
df_inputData.columns

### create the posters
for i in range(0,nrows):
    text_slno = str(df_inputData['SlNo'][i])
    text_title = df_inputData['Title'][i]
    text_content = df_inputData['Content'][i]
    benefit_flag = df_inputData['BenefitFlag'][i]
    overlayimagePath = f"{imagePath}\\{text_slno}.jpg"

    if benefit_flag == 0:
        templatePath0 = f"{templatePath}\\WhispersTemp.jpg"
        modified_image = add_sl_to_image(image_path=templatePath0,text=text_slno,font_size=250,text_position=(204,150),text_color=(227,29,76))
        title_image = add_title_to_image(modified_image,text=text_title,font_size=105,text_position=(510,630),text_color=(227,29,76))
        overlay_image = add_overlay_image(title_image,overlayimagePath,resize = (1700,990), overlay_position=(530,820))
        textbox_image = draw_textbox(image=overlay_image,text=text_content,box_position=(475,2015),box_size=(1850,2000),font_size=75,text_color=(32,27,83),line_space=105)
    else:
        templatePath1 = f"{templatePath}\\WhispersTempBenefits.jpg"
        modified_image = add_sl_to_image(image_path=templatePath1,text=text_slno,font_size=250,text_position=(204,150),text_color=(227,29,76))
        title_image = add_title_to_image(modified_image,text=text_title,font_size=105,text_position=(510,830),text_color=(32,27,83))
        overlay_image = add_overlay_image(title_image,overlayimagePath,resize = (1700,990), overlay_position=(530,1030))
        textbox_image = draw_textbox(image=overlay_image,text=text_content,box_position=(475,2170),box_size=(1850,2000),font_size=75,text_color=(32,27,83),line_space=105)

    # Convert and Save Final Image
    textbox_image = textbox_image.convert('RGB')
    outputImagePath = f"{outputPath}\\Mar_Whisper_{text_slno}.jpg"
    textbox_image.save(outputImagePath)
