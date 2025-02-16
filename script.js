document.getElementById("generateButton").addEventListener("click", async () => {
    const files = document.getElementById("imageUpload").files;
    const prompt = document.getElementById("prompt").value;

    if (files.length === 0 || !prompt) {
        alert("Please upload images and enter a prompt.");
        return;
    }

    const formData = new FormData();
    for (let i = 0; i < files.length; i++) {
        formData.append("images", files[i]);
    }
    formData.append("prompt", prompt);

    try {
        const response = await fetch("http://localhost:5000/generate", {
            method: "POST",
            body: formData,
        });
        const data = await response.json();
        if (data.imageUrl) {
            document.getElementById("outputImage").src = data.imageUrl;
        } else {
            alert("Error generating image.");
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred. Please try again.");
    }
});