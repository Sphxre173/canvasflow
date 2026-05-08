const img_input = document.getElementById("imageInput")
const preview = document.getElementById("preview")

img_input.addEventListener("change", function() {
    const file = img_input.files[0]
    console.log(file)
    if (file) {
        preview.src = URL.createObjectURL(file);
    }
})