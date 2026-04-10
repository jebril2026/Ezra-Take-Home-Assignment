## Card Data for Testing Payments
## https://docs.stripe.com/testing?testing-method=card-numbers#declined-payments

CARD_TEST_DATA_SUCCESS = {
    "visa": {
        "number": "4242424242424242",
        "cvc": "123",
        "expiration_date": "12/30",
        "brand": "Visa"
    },
    "visa_debit": {
        "number": "4000056655665556",
        "cvc": "123",
        "expiration_date": "12/30",
        "brand": "Visa (debit)"
    },
    "mastercard": {
        "number": "5555555555554444",
        "cvc": "123",
        "expiration_date": "12/30",
        "brand": "Mastercard"
    },
    "mastercard_2_series": {
        "number": "2223003122003222",
        "cvc": "123",
        "expiration_date": "12/30",
        "brand": "Mastercard (2-series)"
    },
}

# Declined card test data (simulate failed payments)
CARD_TEST_DATA_DECLINED = {
    "generic_decline": {
        "number": "4000000000000002",
        "cvc": "123",
        "expiration_date": "12/30",
        "error_description": "Your card was declined."
    },
    "insufficient_funds": {
        "number": "4000000000009995",
        "cvc": "123",
        "expiration_date": "12/30",
        "error_description": "Insufficient funds"
    }
}
