from PIL import Image
img = Image.open('page1.jpg')
img_width, img_height = img.size
use_pages=3
new_img = Image.new('RGB', (img_width, img_height * use_pages))
for page_num in range(use_pages):
    img = Image.open(f'page{page_num + 1}.jpg')
    new_img.paste(img, (0, img_height * page_num))
new_img.save('jpgdata.jpg')