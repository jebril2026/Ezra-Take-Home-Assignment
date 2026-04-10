# Submission Guide

This section summarizes where to find answers to each assessment question and the location of all key files:

---

**Question 1: Booking Flow Test Cases**
- Part 1 (15 test cases): [tests/manual/question_1_part_1_and_part_2/member_booking.feature](tests/manual/question_1_part_1_and_part_2/member_booking.feature)
- Part 2 (Top 3 explanations): [docs/question_1_explanations.md](docs/question_1_explanations.md)

**Question 2: Privacy & Security Test**
- Part 1 & 2 (integration test case & HTTP requests): [tests/manual/question_2_part_1_and_part_2/begin_medical_questionnaire.feature](tests/manual/question_2_part_1_and_part_2/begin_medical_questionnaire.feature)
- Part 3 (security test design): [docs/security_test_design.md](docs/security_test_design.md)

**Automated Tests:**
- All automated test code: [tests/](tests/)
- Page objects: [pages/](pages/)
- Test data / Utils / config: [utils/](utils/)

# Ezra Take-Home Assessment - Playwright Python

## Overview
This repository contains a lightweight Playwright + Python automation framework built for Ezra's take-home assessment.

The project uses:
- Playwright
- Pytest
- Page Object Model (POM)
- pytest-xdist (for parallel test execution)

# Definition of Done (DOD)
This project is considered complete when all of the following are true:

- All parts of Question 1, 2, and 3 are fully and properly answered, as outlined in the Submission Guide above.
- The automated test suite is robust and can be run 10 times consecutively (e.g., with `pytest --count=10`) without any failures or flakiness.

## Why I chose this structure
I used a lightweight Page Object Model to keep the tests readable, maintainable, and easy to walk through live. Since the assignment requested a scalable structure, I separated page behavior, test scenarios, and reusable configuration.

I was tempted to build a full-blown BDD framework (since I wrote my test cases in Gherkin!), but realized you might have expected this in JS or TS. I noticed a comment about async—if you’d like to see an async or JS/TS version, I’m happy to provide that in the future. I hope this Python implementation still meets your expectations!


## Trade-offs and assumptions
- The framework is implemented in Python with Playwright and Pytest for maximum readability and maintainability, even though the industry standard for Playwright is often JS/TS. This was a conscious choice to showcase Python automation skills and keep the codebase accessible to Python-focused teams.
- Test data is generated and managed in-memory for speed and simplicity; in a larger or production-grade framework, a more robust test data management strategy would be used.
- The test suite focuses on the core booking and payment flows, with negative and edge cases prioritized for manual or future automated coverage.
- Some selectors (e.g., for Stripe iframes or dynamic elements) are as robust as possible given the current DOM, but may require updates if the UI changes or third-party integrations are updated.
- The framework uses a synchronous Playwright API for simplicity, but can be refactored to async or JS/TS if required.
- Security and privacy test cases are based on observed UI and API behavior, but deeper backend or network-layer validation would require additional access and further app insight.


## Why I chose these test cases

- Because I wanted to showcase a durable test flow for both the happy path and negative path in the most crucial part of the app—booking.

## Future improvements
If this were expanded further, I would add:
- Stronger environment management
- Reusable authentication fixtures
- API-layer tests for backend validation
- CI integration and reporting
- More robust test data management
- Expanded negative and security-focused UI/API coverage
- BDD layer for behavior-driven development
- Monorepo structure to cover web, API, iOS, and Android in a single repo
- Additional integrations (e.g., Twilio for real OTP handling)
- gRPC support if needed
- mTLS for enhanced security on critical API paths
- Kafka testing for event-driven workflows

---
# Prerequisites

Before running the setup script, ensure you have the following installed:

- [Homebrew](https://brew.sh/) (macOS package manager)
- Python (recommended via asdf)
- asdf version manager

### Install Homebrew (if not already installed)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Install asdf and Python
```bash
brew install asdf
asdf plugin-add python
asdf install python latest
asdf global python <latest-version>
```

After installing, restart your terminal or ensure asdf is initialized in your shell profile (see [asdf docs](https://asdf-vm.com/guide/getting-started-legacy.html#_3-install-asdf)).


## Setup

Run the automated setup script (recommended) — please ensure pre-req steps have been completed:

```bash
python setup.py
```

Or, open [setup.py](setup.py) in VS Code and click the play ▶️ button at the top right to run it directly.

This will:
- Create a virtual environment in `.venv`
- Install all dependencies
- Install Playwright browsers
- Validate your environment
- Run a smoke test

After setup, activate the environment:
```bash
source .venv/bin/activate
```

Then run tests as needed:

- To run all tests (all files named test_*.py):
	```bash
	pytest
	```

- To run a specific test file (e.g., the smoke test):
	```bash
	pytest tests/automation/install_smoke.py
	```

- To run a specific test function within a file:
	```bash
	pytest path/to/test_file.py::test_function_name

	eg:
	pytest tests/automation/test_member_booking.py::test_verify_member_can_complete_booking_with_valid_card

	eg:
	pytest tests/automation/test_member_booking.py::test_verify_payment_is_declined_when_member_enters_invalid_card_payment_details
	```

> **Note:** Running tests in parallel locally can be less stable than in CI, depending on your machine's resources. If you see flakiness, try reducing the number of workers with `-n`, but we only have 2 cukes lol - also I just added this to show capability and thinking process, but did not fully work out the kinks. We can obviously stagger them or add some capability to run them a bit differently..

- To run tests in parallel (all test files):
	```bash
	pytest -n auto
	```

- To run a specific test file in parallel:
	```bash
	pytest -n auto tests/automation/test_member_booking.py
	```

- To specify the number of parallel workers (e.g., 4):
	```bash
	pytest -n 4
	```

- To run a specific test function within a file:
	```bash
	pytest path/to/test_file.py::test_function_name

	eg:
	pytest tests/automation/test_member_booking.py::test_verify_member_can_complete_booking_with_valid_card

	eg:
	pytest tests/automation/test_member_booking.py::test_verify_payment_is_declined_when_member_enters_invalid_card_payment_details
	```

- To run a test multiple times (to check for flakiness, requires pytest-repeat):
	```bash
	pytest --count=10 path/to/test_file.py::test_function_name
	```