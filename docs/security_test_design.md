
# Question 2 - Part 3: Security Quality Strategy

This section addresses Part 3 of Question 2: the overall security quality strategy for preventing unauthorized access to sensitive medical data.

## Security Testing Strategy for Sensitive Endpoints

When managing security for 100+ endpoints, relying solely on end-to-end (E2E) testing is not scalable or efficient. The best approach is to shift security testing left also known as the (shift left process), starting as close to the code as possible and layering up to E2E.

**Key Principles:**
- **Unit tests** for authorization logic: Ensure that permission checks and resource access controls are correct at the code level.
- **Integration tests** for endpoints: Validate authentication, authorization, and sensitive data handling in a running service.
- **Contract tests**: Catch unexpected changes in endpoint responses, especially accidental exposure of sensitive fields.
- **E2E tests**: Maintain a small, high-value set for critical user flows (e.g., booking, payment, medical questionnaire). E2E is the final validation, not the only layer.
- **Reusable security checks**: Standardize tests for unauthenticated requests, cross-user access attempts, and field-level data validation across endpoints.
- **Logging and monitoring**: Implement monitoring for unauthorized attempts and unusual access patterns to catch what tests might miss.

**Tradeoffs and Risks:**
- Relying only on shared patterns can miss endpoint-specific edge cases.
- Unit, contract, and integration tests provide fast feedback but don’t fully replace E2E coverage.
- Too much E2E testing slows feedback and increases brittleness.

**Balanced Strategy:**
- Catch as much as possible early with unit, contract, and integration tests.
- Use E2E tests to validate the most critical end-to-end flows and ensure the system works as a whole.

---

*This approach ensures security is built in at every layer, not just tested at the end.*
