from PIL import Image, ImageEnhance
from pathlib import Path
import pytesseract
import os

#pytesseract.pytesseract.tesseract_cmd = 

#data_folder = Path("image_scans")
#rel_path = "bug_catcher.jpg"

#script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
#rel_path = "2091/data.txt"
#abs_file_path = os.path.join(script_dir, rel_path)

path = r"C:\Users\br200\Desktop\tcg cmd edition\image_scans\cropped"
save_path = r"ai_image"

os.chdir(r"C:\Users\br200\Desktop\tcg cmd edition\image_scans\cropped")

directories = os.listdir(path)

for file in directories:
    img = Image.open(file)

    '''
    enhancer1 = ImageEnhance.Sharpness(img)
    enhancer2 = ImageEnhance.Contrast(img)

    img_edit = enhancer1.enhance(20.0)
    img_edit = enhancer2.enhance(1.5)
    '''
    
    #img_edit.save(f"{file}.jpg")

    result = pytesseract.image_to_string(img)

    with open(f'{file}.txt', mode ='w') as file:
        file.write(result)
        print(f"{file} completed!")


'''
print(rel_path)



# adding some sharpness and contrast to the image 
enhancer1 = ImageEnhance.Sharpness(img)
enhancer2 = ImageEnhance.Contrast(img)

img_edit = enhancer1.enhance(20.0)
img_edit = enhancer2.enhance(1.5)

# save the new image
img_edit.save("edited_image.png")



# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img)

# converts the image to result and saves it into result variable
result = pytesseract.image_to_string(img_edit)

with open('text_result.txt', mode ='w') as file:
 file.write(result)
 print("ready!")
 '''