document.addEventListener('DOMContentLoaded', () => {
    const paymentItemCards = document.querySelectorAll('.payment-item-card');
    const summarySubtotalEl = document.getElementById('summary-subtotal');
    const summaryTaxesEl = document.getElementById('summary-taxes');
    const summaryTotalEl = document.getElementById('summary-total');
    const paymentForm = document.getElementById('payment-form');
    const paymentMessage = document.getElementById('payment-message');
    
    const TAX_RATE = 0.05; // 5% tax

    // Function to calculate and update the subtotal for a single item
    const updateItemSubtotal = (card) => {
        const variantSelect = card.querySelector('.item-variant');
        const quantityInput = card.querySelector('.item-quantity');
        const subtotalEl = card.querySelector('.item-subtotal');

        const price = parseFloat(variantSelect.value);
        const quantity = parseInt(quantityInput.value);
        const subtotal = price * quantity;

        if (subtotalEl) {
            subtotalEl.textContent = `GHS ${subtotal.toFixed(2)}`;
        }
        
        updateOrderSummary();
    };

    // Function to calculate and update the main order summary
    const updateOrderSummary = () => {
        let totalSubtotal = 0;
        paymentItemCards.forEach(card => {
            const variantPrice = parseFloat(card.querySelector('.item-variant').value);
            const quantity = parseInt(card.querySelector('.item-quantity').value);
            totalSubtotal += variantPrice * quantity;
        });

        const taxes = totalSubtotal * TAX_RATE;
        const total = totalSubtotal + taxes;

        if (summarySubtotalEl) summarySubtotalEl.textContent = `GHS ${totalSubtotal.toFixed(2)}`;
        if (summaryTaxesEl) summaryTaxesEl.textContent = `GHS ${taxes.toFixed(2)}`;
        if (summaryTotalEl) summaryTotalEl.textContent = `GHS ${total.toFixed(2)}`;
    };

    // Add event listeners to all item cards
    paymentItemCards.forEach(card => {
        const variantSelect = card.querySelector('.item-variant');
        const quantityInput = card.querySelector('.item-quantity');

        variantSelect.addEventListener('change', () => updateItemSubtotal(card));
        quantityInput.addEventListener('input', () => updateItemSubtotal(card));
    });

    // Handle payment form submission
    if (paymentForm) {
        paymentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (paymentMessage) {
                paymentMessage.textContent = 'Processing your payment...';
                paymentMessage.style.color = 'var(--accent-primary)';

                // Simulate processing delay
                setTimeout(() => {
                    paymentMessage.textContent = 'Payment successful! Thank you for your order.';
                    paymentMessage.style.color = 'var(--success-green)';
                    paymentForm.reset();
                }, 2000);
                 setTimeout(() => {
                    paymentMessage.textContent = '';
                }, 7000);
            }
        });
    }

    // Initial calculation on page load
    updateOrderSummary();
});