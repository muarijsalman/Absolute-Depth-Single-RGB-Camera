from PIL import Image

# Open the image
image = Image.open("testing_images1\\33.64334,72.99055.png")

# Set the desired size for the output image
new_size = (1280, 704)  # Width, Height

# Resize the image
resized_image = image.resize(new_size)

# Save the resized image
resized_image.save("testing_images1\\33.64334,72.99055.png")
