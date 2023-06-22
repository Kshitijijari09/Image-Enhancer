# from PIL import Image


# def upscale_image(input_image_path, output_image_path):
#     # Open the low-quality image
#     image = Image.open(input_image_path)

#     # Calculate the scaling factor
#     width, height = image.size
#     scale_factor = 1920 / width

#     # Calculate the new height while maintaining the aspect ratio
#     new_height = round(height * scale_factor)

#     # Resize the image using nearest-neighbor algorithm
#     image = image.resize((1920, new_height), resample=Image.NEAREST)

#     # Create a new white canvas with HD 1080p resolution
#     new_image = Image.new("RGB", (1920, 1080), "white")

#     # Calculate the position to paste the upscaled image
#     x = 0
#     y = (1080 - new_height) // 2

#     # Paste the upscaled image onto the canvas
#     new_image.paste(image, (x, y))

#     # Save the generated HD image
#     new_image.save(output_image_path)

#     print("Image upscaled successfully!")


# # Usage example
# input_image = "WP_20150519_002_Original_Original.jpg"
# output_image = "test.jpg"
# upscale_image(input_image, output_image)

'''The code I provided resizes the image to the desired HD resolution of 1920x1080 pixels, but it uses the nearest-neighbor algorithm, which does not effectively upscale the image's quality.

To improve the upscaling quality, we can use a different resampling algorithm, such as Lanczos interpolation. Here's an updated version of the code that uses Lanczos interpolation for better results:'''

from PIL import Image
iteration = 100000
def upscale_image(input_image_path, output_image_path):
    # Open the low-quality image
    image = Image.open(input_image_path)

    # Calculate the scaling factor
    width, height = image.size
    scale_factor = 1920 / width

    # Calculate the new height while maintaining the aspect ratio
    new_height = round(height * scale_factor)

    # Resize the image using Lanczos interpolation
    for i in range(iteration):
        image = image.resize((1920, new_height), resample=Image.LANCZOS)
        print(i)
    # Create a new white canvas with HD 1080p resolution
    new_image = Image.new("RGB", (1920, 1080), "white")

    # Calculate the position to paste the upscaled image
    x = 0
    y = (1080 - new_height) // 2

    # Paste the upscaled image onto the canvas
    new_image.paste(image, (x, y))

    # Save the generated HD image
    new_image.save(output_image_path)

    print("Image upscaled successfully!")


# Usage example
input_image = "WP_20150519_002_Original_Original.jpg"
output_image = "E1.jpg"
upscale_image(input_image, output_image)
