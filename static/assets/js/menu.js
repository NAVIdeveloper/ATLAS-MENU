document.addEventListener('DOMContentLoaded', () => {
    // Get all quantity controls
    const productCards = document.querySelectorAll('.ios-product-card');
    productCards.forEach(card => {
        const decreaseBtn = card.querySelector('.quantity-btn.decrease');
        const increaseBtn = card.querySelector('.quantity-btn.increase');
        const quantityValue = card.querySelector('.quantity-value');
        const quantityForm = card.querySelector('#quantity-hidden');

        decreaseBtn.addEventListener('click', () => {
            let currentValue = parseInt(quantityValue.textContent);
            if (currentValue > 0) {
                quantityValue.textContent = currentValue - 1;
                quantityForm.value = currentValue - 1;
            }
        });

        increaseBtn.addEventListener('click', () => {
            let currentValue = parseInt(quantityValue.textContent);
            if (currentValue < 11) {
                quantityValue.textContent = currentValue + 1;
                quantityForm.value = currentValue + 1;
            }
        });
    });
});