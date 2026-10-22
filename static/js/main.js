/**
 * static/js/main.js
 * Clean Vanilla JavaScript for ClothStore UI Interactions
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto dismiss or close flash alert messages
    const alertCloseButtons = document.querySelectorAll('.alert-close');
    alertCloseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const alert = button.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 250);
            }
        });
    });

    // Automatically fade out success alerts after 5 seconds
    const successAlerts = document.querySelectorAll('.alert-success');
    successAlerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.transition = 'opacity 0.5s ease';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 500);
            }
        }, 5000);
    });

    // 2. Demo Payment Card formatting (Groups of 4 digits)
    const cardNumberInput = document.getElementById('demoCardNumber');
    if (cardNumberInput) {
        cardNumberInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 16);
            let formatted = val.match(/.{1,4}/g)?.join(' ') || val;
            e.target.value = formatted;
            
            // Mirror to card preview
            const previewNum = document.getElementById('previewCardNumber');
            if (previewNum) {
                previewNum.textContent = formatted || '•••• •••• •••• ••••';
            }
        });
    }

    const cardHolderInput = document.getElementById('demoCardHolder');
    if (cardHolderInput) {
        cardHolderInput.addEventListener('input', (e) => {
            const previewHolder = document.getElementById('previewCardHolder');
            if (previewHolder) {
                previewHolder.textContent = e.target.value.toUpperCase() || 'CARDHOLDER NAME';
            }
        });
    }

    const cardExpiryInput = document.getElementById('demoCardExpiry');
    if (cardExpiryInput) {
        cardExpiryInput.addEventListener('input', (e) => {
            let val = e.target.value.replace(/\D/g, '').substring(0, 4);
            if (val.length >= 2) {
                val = val.substring(0, 2) + '/' + val.substring(2);
            }
            e.target.value = val;
            const previewExpiry = document.getElementById('previewCardExpiry');
            if (previewExpiry) {
                previewExpiry.textContent = val || 'MM/YY';
            }
        });
    }

    // 3. Confirm remove from cart
    const removeLinks = document.querySelectorAll('.confirm-remove');
    removeLinks.forEach(link => {
        link.addEventListener('click', (e) => {
            if (!confirm('Are you sure you want to remove this item from your cart?')) {
                e.preventDefault();
            }
        });
    });
});
