import streamlit as st
import cv2


def pencil_sketch(image_path):
    # Read the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Invert the grayscale image
    inverted_gray_img = 255 - gray_img

    # Blur the inverted image using Gaussian blur
    blurred_img = cv2.GaussianBlur(inverted_gray_img, (21, 21), 0)

    # Invert the blurred image
    inverted_blurred_img = 255 - blurred_img

    # Create the pencil sketch image by combining the inverted blurred image with the original grayscale image
    pencil_sketch_img = cv2.divide(gray_img, inverted_blurred_img, scale=256.0)

    return pencil_sketch_img

def cartoonify(image_path):
    # Read the image
    original_image = cv2.imread(image_path)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    # Convert image to grayscale
    gray = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

    # Apply median blur to smoothen the image
    smooth_gray = cv2.medianBlur(gray, 5)

    # Detect edges using adaptive thresholding
    edges = cv2.adaptiveThreshold(smooth_gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)

    # Apply bilateral filter to reduce noise while preserving edges
    color = cv2.bilateralFilter(original_image, 9, 300, 300)

    # Combine color image with edges
    cartoon_image = cv2.bitwise_and(color, color, mask=edges)

    return cartoon_image

def image_transformation_page():
    st.title('Image Transformation')

    transformation_type = st.radio("Select transformation type:", ("Pencil Sketch", "Cartoonify"))

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    st.text('OR')
    cap = st.camera_input('Capture an image')
    if uploaded_file is not None:
        uploaded_file = uploaded_file
    if cap is not None:
        uploaded_file = cap

    if uploaded_file is not None:
        # Save the uploaded file to a temporary directory
        temp_image_path = 'temp_image.' + uploaded_file.name.split('.')[-1]
        with open(temp_image_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())

        # Display the original image
        original_img = cv2.imread(temp_image_path)
        st.image(cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB), caption='Original Image', use_column_width=True)

        if transformation_type == "Pencil Sketch":
            # Convert the uploaded image to pencil sketch when the "Convert to Sketch" button is clicked
            if st.button('Convert to Pencil Sketch'):
                # Convert the uploaded image to pencil sketch
                pencil_sketch_img = pencil_sketch(temp_image_path)

                # Display the pencil sketch image
                st.image(cv2.cvtColor(pencil_sketch_img, cv2.COLOR_BGR2RGB), caption='Pencil Sketch', use_column_width=True)

                # Save the pencil sketch image
                st.write("### Save Pencil Sketch")
                save_path = 'pencil_sketch.png'
                cv2.imwrite(save_path, pencil_sketch_img)
                with open(save_path, 'rb') as f:
                    file_bytes = f.read()
                st.download_button(label='Click here to download the image',
                                   data=file_bytes,
                                   file_name='pencil_sketch.png',
                                   mime='image/png')

        elif transformation_type == "Cartoonify":
            # Process the uploaded image when the "Convert to Cartoon" button is clicked
            if st.button('Convert to Cartoon'):
                # Process the uploaded image
                cartoon_image = cartoonify(temp_image_path)

                # Display the processed image
                st.image(cartoon_image, caption='Cartoonified Image', use_column_width=True, channels="RGB")

                # Save the processed image
                st.write("### Save Cartoonified Image")
                save_path = 'cartoonified_image.png'
                cv2.imwrite(save_path, cv2.cvtColor(cartoon_image, cv2.COLOR_RGB2BGR))
                with open(save_path, 'rb') as f:
                    file_bytes = f.read()
                st.download_button(label='Click here to download the image',
                                   data=file_bytes,
                                   file_name='cartoonified_image.png',
                                   mime='image/png')

def about_page():
    # Define the title text with HTML and CSS styling
    title_text = (
        "<h1 style='"
        "color: orange;"  # Set color to orange for "ArtWizard"
        "font-family: Pacifico, cursive;"  # Use Sacramento font
        "font-size: 48px;"  # Set font size
        "'>"
        "ArtWizard: "
        "<span style='color: blue;'>"  # Set color to blue for "Cartoon & Sketch"
        "Cartoon & Sketch "
        "</span>"
        "<span style='color: #2E8B57;'>"  # Set color to Parrot Green for "Transformation Tool"
        "Transformation Tool"
        "</span>"
        "</h1>"
    )

    # Display the title using st.markdown
    st.markdown(title_text, unsafe_allow_html=True)

    thumbnail_image = 'Untitled design.png'  # Path to your thumbnail image
    st.image(thumbnail_image, use_column_width=True)

    st.write("""
    This is an image transformation app where you can convert your images to pencil sketches or cartoonified images. 
    It provides an intuitive interface to upload images, apply transformations, and save/download the transformed images.    
    """)

    st.header('Workflow:')
    st.write("""
        1. Upload an image using the file uploader.
        2. Select the transformation type: Pencil Sketch or Cartoonify.
        3. Click the corresponding button to apply the transformation.
        4. Optionally, you can save or download the transformed image.
        """)

    st.header('Connect with Me:')
    st.write("""
    If you have any questions or feedback, feel free to connect with me on [GitHub](https://github.com/kuldeepprajapati-dev) or [LinkedIn](https://www.linkedin.com/in/kuldeep-kumar-prajapati/).
    """)

def main():
    page = st.sidebar.selectbox("Select page:", ("About", "Image Transformation"))

    if page == "About":
        about_page()

    elif page == "Image Transformation":
        image_transformation_page()

if __name__ == '__main__':
    main()
