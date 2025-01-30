document.getElementById('imageUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function(event) {
            const img = document.getElementById('preview-image');
            img.src = event.target.result;
            img.style.display = 'block';
            document.querySelector('.bx-cloud-upload').style.display = 'none';
            document.querySelector('.img-area h3').style.display = 'none';
            document.querySelector('.img-area p').style.display = 'none';
        }
        reader.readAsDataURL(file);
    }
});

document.getElementById('btn-predict').addEventListener('click', function() {
    const fileInput = document.getElementById('imageUpload');
    if (!fileInput.files[0]) {
        alert('Please select an image first');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Show loader
    document.querySelector('#loader').style.display = 'block';
    document.getElementById('prediction-result').textContent = '';

    fetch('/analyze_disease', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())  // Expecting JSON response
    .then(data => {
        document.querySelector('#loader').style.display = 'none'; // Hide loader
        document.getElementById('prediction-result').textContent = `${data.prediction}`;
    })
    .catch(error => {
        console.error('Error:', error);
        document.querySelector('#loader').style.display = 'none';
        document.getElementById('prediction-result').textContent = 'Error analyzing image';
    });
});
