---
name: java-e2e
description: End-to-end testing for Java/Spring Boot projects with SQLite, Thymeleaf, and Spring Security. Analyzes pom.xml dependencies, scans REST controllers, generates E2E tests with RestAssured/MockMvc, runs tests with coverage reports.
---

# Java E2E Testing Skill

End-to-end testing assistant for Java/Spring Boot applications.

## Capabilities

This skill helps you:

1. **Analyze Project Structure**
   - Scans `pom.xml` for dependencies (Spring Boot, testing frameworks, databases)
   - Identifies REST controllers and their endpoints
   - Detects database configurations (SQLite, MySQL, etc.)

2. **Generate E2E Tests**
   - Creates comprehensive test cases using RestAssured or MockMvc
   - Tests REST API endpoints automatically
   - Includes authentication testing (Spring Security)
   - Generates tests for CRUD operations

3. **Setup Test Infrastructure**
   - Configures test databases (H2, Testcontainers, etc.)
   - Sets up test properties in `application-test.yml`
   - Configures RestAssured or MockMvc

4. **Run and Report**
   - Executes E2E tests
   - Generates coverage reports (JaCoCo)
   - Provides test execution summaries

## Usage

Simply invoke this skill when working with a Java/Spring Boot project:

```
"Generate E2E tests for this Spring Boot project"
"Set up end-to-end testing for my API"
"Run E2E tests and show coverage"
```

## Dependencies Detected

- Spring Boot Test
- RestAssured (for API testing)
- MockMvc (Spring MVC testing)
- JUnit 5 / Jupiter
- Spring Security (if applicable)
- Database drivers (SQLite, MySQL, etc.)

## Test Pattern

Generated tests follow this pattern:

1. **Setup**: Configure test context and database
2. **Authentication**: Login and obtain session/token
3. **Test Cases**:
   - GET endpoints (list, detail)
   - POST endpoints (create)
   - PUT/PATCH endpoints (update)
   - DELETE endpoints (delete)
4. **Cleanup**: Restore test data state

## Test Location

Tests are generated in: `src/test/java/com/<package>/e2e/`
