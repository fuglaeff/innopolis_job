function card(stripe_publishable_key) {
  document.addEventListener("DOMContentLoaded", function(event){
      var stripe = Stripe(stripe_publishable_key);
      var elements = stripe.elements();

      var style = {
        base: {
          color: '#32325d',
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
      card.mount("#card-element");

     var form = document.getElementById('payment-form');
     form.addEventListener('submit', function(event) {
        event.preventDefault();
            stripe.createPaymentMethod({
              type: 'card',
              card: card,
            }).then(function(payment_method_result){ 
              if (payment_method_result.error) {
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = payment_method_result.error.message;
              } else {
                var form = document.getElementById('payment-form');
                var hiddenInput = document.createElement('input');

                hiddenInput.setAttribute('type', 'hidden');
                hiddenInput.setAttribute('name', 'payment_method_id');
                hiddenInput.setAttribute('value', payment_method_result.paymentMethod.id);

                form.appendChild(hiddenInput);
                form.submit();
              };
            });

     });

  })
};