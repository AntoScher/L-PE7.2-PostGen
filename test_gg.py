from generators.image_gen_gg import ImageGenerator
import config as conf

img_desc = "A futuristic cityscape at sunset"
img_gen = ImageGenerator(conf.google_api_key)
try:
    image_url = img_gen.generate_image(img_desc)
    print(image_url)
except Exception as e:
    print(f"Error: {e}")
