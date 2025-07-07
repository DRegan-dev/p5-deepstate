var stripePublicKey = document.getElementById('id_stripe_public_key').textContent.slice(1, -1);
var clientSecret = document.getElementById('id_client_secret').textContent.slice(1, -1);
var stripe = Stripe(stripePublicKey);
var elements = stripe.elements();

var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
        color: '#aab7c4'
        }
    },
    invalid: {
        color: '#fa755a',
        iconColor: '#fa755a'
    }
};
var card = elements.create('card', {style: style});
card.mount('#card-element');

// Handle realtime validation errors on the card element
card.addEventListener('change', function (event) {
    var errorDiv = document.getElementById('card-errors');
    if (event.error) {
        var html = `
            <span class="icon" role="alert">
                <i class="fas fa-times"></i>
            </span>
            <span>${event.error.message}</span>
            `;    
            errorDiv.innerHTML = html;  
    } else {
        errorDiv.textContent = '';
    }
});

//Utility functions for animations
function fadeOut(element, duration = 300) {
    element.style.opacity = '1';
    element.style.transition = `opacity ${duration}ms`;
    element.style.opacity = '0';
    
    setTimeout(() => {
        element.style.display = 'none';
    }, duration);
}

function fadeIn(element, duration = 300) {
    element.style.display = 'block';
    element.style.opacity = '0';
    element.style.transition = `opacity ${duration}ms`;
    setTimeout(() => {
        element.style.opacity = '1';
    }, 10);
}

function fadeToggle(element, duration = 300) {
    if (element.style.display === 'none' || element.style.display === '') {
        fadeIn(element, duration);
    } else {
        fadeOut(element, duration);
    }
}

// Handle form submit
var form = document.getElementById('payment-form');
form.addEventListener('submit', function(ev) {
    ev.preventDefault();
    card.update({'disabled': true});
    
    document.getElementById('submit-button').disabled = true;
    document.getElementById('submit-button').innerHTML = 'Processing...';

    console.log('Form fields check:');
    console.log('full_name', form.phone_number);
    console.log('phone_number:', form.phone_number);
    console.log('email:', form.email);
    console.log('street_address1', form.street_address1);
    console.log('sreet_address2:', form.street_address2);
    console.log('town_or_city:', form.town_or_city);
    console.log('country', form.country);
    console.log('county', form.county);
    console.log('postcode', form.postcode);

    const billingDetails = {};
    const nameField = form.querySelector('[name="full_name"]');
    const phoneField = form.querySelector('[name="phone_number"]');
    const emailField = form.querySelector('[name="email"]');
    const address1Field = form.querySelector('[name="street_address1"]');
    const address2Field = form.querySelector('[name="street_address2"]');
    const cityField = form.querySelector('[name="town_or_city"]');
    const countryField = form.querySelector('[name="country"]');
    const postcodeField = form.querySelector('[name="postcode"]');

    if (nameField && nameField.value.trim()) {
        billingDetails.name = nameField.value.trim();
    }
    if (phoneField && phoneField.value.trim()) {
        billingDetails.phone = phoneField.value.trim();
    }
    if (emailField && emailField.value.trim()) {
        billingDetails.email = emailField.value.trim();
    }

    // Build address object only if we have required fields
    const addressData = {};
    if (address1Field && address1Field.value.trim()) {
        addressData.line1 = address1Field.value.trim();
    }

    if (address2Field && address2Field.value.trim()) {
        addressData.line1 = address2Field.value.trim();
    }

    if (cityField && cityField.value.trim()) {
        addressData.city = cityField.value.trim();
    }

    if (countryField && countryField.value.trim()) {
        addressData.country = countryField.value.trim().toUpperCase();
    }

    if (postcodeField && postcodeField.value.trim()) {
        addressData.postal_code = postcodeField.value.trim();
    }

    // Only include address if we have at least line1
    if (addressData.line1) {
        billingDetails.address = addressData;
    }

    // Build shipping object only if we have required fields
    const shippingData = {};
    if (nameField && nameField.value.trim()) {
        shippingData.name = nameField.value.trim();
    }
    if (phoneField && phoneField.value.trim()) {
        shippingData.phone = phoneField.value.trim();
    } 

    // Build Shipping address
    const shippingAddress = {};
    if (address1Field && address1Field.value.trim()) {
        shippingAddress.line1 = address1Field.value.trim();
    }

    if (address2Field && address2Field.value.trim()) {
        shippingAddress.line2 = address2Field.value.trim();
    }

    if (cityField && cityField.value.trim()) {
        shippingAddress.city = cityField.value.trim();
    }

    if (countryField && countryField.value.trim()) {
        shippingAddress.country = countryField.value.trim().toUpperCase();
    }

    if (postcodeField && postcodeField.value.trim()) {
        shippingAddress.postal_code = postcodeField.value.trim();
    }

    // Only include shipping address if we have required fields
    if (shippingAddress.line1 && shippingData.name) {
        shippingData.address = shippingAddress;
    }

    const confirmationData = {
        payment_method: {
            card: card
        }
    };

    if(Object.keys(billingDetails).length > 0) {
        confirmationData.shipping = shippingData;
    }

    if (Object.keys(shippingData).length > 0 && shippingData.address) {
        confirmationData.shipping = shippingData;
    }

    console.log('Confirmation data:', JSON.stringify(confirmationData, null, 2));

    stripe.confirmCardPayment(clientSecret, confirmationData).then(function(result) {
        if (result.error) {
            var errorDiv = document.getElementById('card-errors');
            var html = `
                <span class="icon" role="alert">
                <i class="fas fa-times"></i>
                </span>
                <span>${result.error.message}</span>`;
            errorDiv.innerHTML = html;
            card.update({ 'disabled': false});
            document.getElementById('submit-button').disabled = false;
            document.getElementById('submit-button').innerHTML = 'Complete Order<i class="fas fa-lock ms-2"></i>';
        } else {
            console.log('Payment Intent Status:', result.paymentIntent.status);
            if (result.paymentIntent.status === 'succeeded') {
                console.log('Payment succeeded, submitting form...');
                console.log('Form action:', form.action);
                console.log('Form method:', form.method);
                form.submit();
            }
        }
    });
});