// Modal functionality
document.addEventListener('DOMContentLoaded', function() {
    // Get the add product button by its ID
    const addProductBtn = document.getElementById('add-product-btn');
    
    if (addProductBtn) {
        addProductBtn.addEventListener('click', () => {
            const modal = document.getElementById('modal-add-new');
            if (modal) {
                modal.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    }

    // Close modal handlers
    document.querySelectorAll('.modal-close-btn, .modal-cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const modal = btn.closest('.ios-modal');
            if (modal) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Close modal when clicking outside
    document.querySelectorAll('.ios-modal').forEach(modal => {
        modal.addEventListener('click', (e) => {
            if (e.target === modal || e.target.classList.contains('modal-overlay')) {
                modal.classList.remove('active');
                document.body.style.overflow = '';
            }
        });
    });

    // Image upload preview (uncomment if needed)
    const fileInput = document.querySelector('.image-upload-container input[type="file"]');
    const uploadPreview = document.querySelector('.upload-preview');

    if (fileInput && uploadPreview) {
        fileInput.addEventListener('change', (e) => {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    uploadPreview.innerHTML = `<img src="${event.target.result}" style="max-width: 100%; max-height: 120px; border-radius: 8px;">`;
                };
                reader.readAsDataURL(file);
            }
        });
    }
});