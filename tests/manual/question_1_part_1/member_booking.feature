## Choose to go with a hybrid BDD approach and not an Imperative or Declarative approach.
@regression @e2e
Feature: Member onboarding and booking flow - Question 1 Part 1 and Part 2

Background: A new member reaches the booking flow
  Given I am on the Ezra member sign-up page
  When I create a new member with valid personal information
  And I accept the terms and conditions
  Then I should be redirected to the Select your plan page

  @P1
  Scenario: verify member can successfully complete booking with valid card information
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan with Skeletal and Neurological Assessment" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $3999
  When I enter valid card payment details
  And I continue
  Then payment is successfully processed
  And I should be redirected to the scan confirmation page
  When I log in to the internal hub portal
  And I search for the member by email address
  Then I should see the member record with the correct booking details
 
 @P1
Scenario: verify member can successfully complete booking using bank payment
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan With Spine" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $1699
  When I select Bank as the payment method
  And I successfully link a valid bank account
  And I enter the OTP for bank account verification
  And I complete bank account verification successfully
  Then the bank account should be successfully linked for payment
  When I continue to submit payment
  Then payment is successfully processed
  And I should be redirected to the scan confirmation page
  And a booking should be created with the correct details
  When I log in to the internal hub portal
  And I search for the member by email address
  Then I should see exactly one booking created with the correct details

  @P1
  Scenario: verify payment is declined when member enters invalid card payment details
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $999
  When I enter declined card payment details
  And I continue
  Then payment should be declined
  And I should see an appropriate payment error message
  And I should remain on the Reserve your appointment page
  And no booking should be created

 @P1
Scenario: verify member cannot complete booking if bank account linking fails
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan with Skeletal and Neurological Assessment" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $3999
  When I select Bank as the payment method
  And I attempt to link a valid bank account
  And I enter the OTP for bank account verification
  But bank account verification does not succeed
  Then the bank account should not be successfully linked for payment
  And I should see an appropriate bank payment error message
  When I attempt to continue to submit payment
  Then payment should not be processed
  And I should remain on the Reserve your appointment page
  And no booking should be created

Scenario: verify member is not charged twice if payment is submitted multiple times
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan With Spine" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $1699
  When I enter valid card payment details
  And I submit payment multiple times
  Then payment should be processed only once
  And only one booking should be created
  And I should be redirected to the scan confirmation page
  When I log in to the internal hub portal
  And I search for the member by email address
  Then I should see the member record with the correct booking details

  Scenario: verify booking is not created if payment confirmation fails
  When I enter the member's date of birth and sex at birth
  And I select the "Heart CT Scan" plan
  And I continue
  And I answer no to the health questionnaire
  And I submit the health questionnaire
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $349
  When payment confirmation fails
  Then payment should not be marked as successful
  And I should remain on the Reserve your appointment page
  And no booking should be created

Scenario: verify member can retry payment after a failed attempt without creating duplicate booking state
  When I enter the member's date of birth and sex at birth
  And I select the "Lung CT Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $399
  When I enter declined card payment details
  And I continue
  Then payment should be declined
  And I should see an appropriate payment error message
  And I should remain on the Reserve your appointment page
  When I enter valid card payment details
  And I continue
  Then payment is successfully processed
  And I should be redirected to the scan confirmation page
  And only one booking should be created
  And only one charge should be recorded
  When I log in to the internal hub portal
  And I search for the member by email address
  Then I should see the member record with the correct booking details

Scenario: verify booking state remains consistent when payment succeeds but confirmation page fails to load
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $999
  When I enter valid card payment details
  And I simulate a failure to load the confirmation page after payment submission
  Then payment is successfully processed
  And I should not see duplicate confirmation attempts
  When I log in to the internal hub portal
  And I search for the member by email address
  Then I should see exactly one booking created with the correct details

Scenario: verify member cannot book if the selected slot is taken before payment
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan with Skeletal and Neurological Assessment" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select a specific appointment slot
  And I book the same appointment slot for another member via API
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  When I enter valid card payment details
  And I continue
  Then booking should fail due to slot unavailability
  And I should see an appropriate error message
  And no booking should be created

Scenario: verify member cannot book if network connection is lost during payment
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $999
  When I enter valid card payment details
  And I lose network connection during payment submission
  Then payment should not be confirmed
  And I should see an appropriate error message
  And I should remain on the Reserve your appointment page
  And no booking should be created

Scenario: verify member cannot continue booking if session expires during the flow
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan With Spine" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I simulate an expired member session
  And I attempt to continue to the payment step
  Then I should be redirected to the sign-in page
  And I should see a session expired message
  And no booking should be created

  Scenario: verify required payment fields prevent progression when missing
  When I enter the member's date of birth and sex at birth
  And I select the "Heart CT Scan" plan
  And I continue
  And I answer no to the health questionnaire
  And I submit the health questionnaire
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $349
  When I leave one or more required payment fields blank
  And I attempt to continue
  Then payment should not be processed
  And I should remain on the Reserve your appointment page
  And I should see required field validation messages
  And no booking should be created

  Scenario: verify member cannot book with an invalid card number
  When I enter the member's date of birth and sex at birth
  And I select the "Lung CT Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $399
  When I enter an invalid card number format
  And I continue
  Then payment should not be processed
  And I should see a card number validation error message
  And I should remain on the Reserve your appointment page
  And no booking should be created

  Scenario: verify member cannot book with an expired card
  When I enter the member's date of birth and sex at birth
  And I select the "MRI Scan" plan
  And I continue
  Then I should be redirected to the Schedule your scan page
  When I choose a valid center
  And I select valid appointment availability
  And I continue to the payment step
  Then I should be redirected to the Reserve your appointment page
  And I should see the correct plan total of $999
  When I enter an expired card
  And I continue
  Then payment should be declined
  And I should see an appropriate payment error message
  And I should remain on the Reserve your appointment page
  And no booking should be created

Scenario: verify member cannot proceed if required terms and conditions are not accepted
  Given I am on the Ezra member sign-up page
  When I create a new member with valid personal information
  And I leave the required terms and conditions checkbox unchecked
  And I attempt to submit the form
  Then I should remain on the sign-up page
  And I should see a terms and conditions required message
  And I should not be able to proceed to the Select your plan page
