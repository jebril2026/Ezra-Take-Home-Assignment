@regression @e2e
Feature: Member Medical Questionnaire - Access Control and Data Integrity - Question 2 Part 1 and Part 2

Scenario: verify a member cannot access or modify another member`s medical questionnaire data
Given I create a new member "Member A" with valid personal information
And I complete booking successfully for "Member A"
And I begin the medical questionnaire for "Member A"
And I intercept the questionnaire submission API request:
#  POST https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/3582/data
And I copy the request for further testing - copy as cURL
##
When I create a new member "Member B" with valid personal information
And I complete booking successfully for "Member B"
And I begin the medical questionnaire for "Member B"
And I capture Member B's questionnaire submission_id
When I reuse the API request from Member A
And I replace the submission_id with Member B's submission_id
And I send the request using Member A's authentication token
Then the request should be rejected with a 403 Forbidden
And Member A should not be able to access or modify Member B's questionnaire data
And Member B's questionnaire data should remain unchanged

## Notes / HTTP Requests


## This is a valid request where the authenticated user (Member A) 
## is submitting data to their own medical questionnaire using their own submission_id.

# POST https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{submission_id_A}/data
# Authorization: Bearer <member_A_token>
# Content-Type: application/json

# {
#   "key": "height",
#   "value": "{\"heightFeet\":\"7\",\"heightInches\":\"0\"}",
#   "hasAnswer": true
# }

And 

## In this request, the authentication token still belongs to Member A, 
## but the submission_id has been changed to Member B`s. 
## This simulates an attempt to access or modify another member’s medical data by manipulating the resource identifier.

# POST https://stage-api.ezra.com/diagnostics/api/medicaldata/forms/mq/submissions/{submission_id_B}/data
# Authorization: Bearer <member_A_token>
# Content-Type: application/json

# {
#   "key": "height",
#   "value": "{\"heightFeet\":\"5\",\"heightInches\":\"0\"}",
#   "hasAnswer": true
# }