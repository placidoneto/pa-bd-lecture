package com.seuprojeto;

import io.quarkus.test.junit.QuarkusTest;
import org.junit.jupiter.api.Test;

import static io.restassured.RestAssured.given;

@QuarkusTest
class GreetingResourceTest {
    @Test
    void testAuxilioEndpoint() {
        given()
          .when().get("/auxilio")
          .then()
             .statusCode(200);
    }

}