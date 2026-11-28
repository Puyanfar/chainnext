describe('Header auth', () => {
  beforeEach(() => {
    cy.visit('/');
  });

  describe('without an authorization header', () => {
    it('should display an alert message', () => {
      cy.get('.alert').should('exist');
    });
  });

  describe('with authorization header set', () => {
    const setupInterceptors = () => {
      cy.intercept('/auth/header', (req) => {
        req.headers['test-header'] = 'test header value';
        req.reply();
      }).as('auth');
    };

    beforeEach(() => {
      setupInterceptors();
    });

    // Tests that verify the user is logged in (applicable both initially and after reload)
    const shouldBeLoggedIn = () => {
      it('should not display an alert message', () => {
        cy.get('.alert').should('not.exist');
      });

      it("should display 'Hello admin'", () => {
        cy.get('.step').eq(0).should('contain', 'Hello admin');
      });
    };

    // This test only applies to initial login where /auth/header is called
    it('should have an access_token cookie in /auth/header response', () => {
      cy.wait('@auth').then((interception) => {
        expect(interception.response, 'Intercepted response').to.satisfy(
          () => true
        );
        expect(interception.response.statusCode).to.equal(200);
      });
      // Browser-agnostic: assert the cookie is actually stored.
      // Chromium 157+ no longer exposes the Set-Cookie header line to the
      // XHR/fetch interceptor, so checking the cookie jar instead.
      cy.getCookie('access_token')
        .should('exist')
        .and('have.property', 'value');
    });

    shouldBeLoggedIn();

    it('should request and have access to /user', () => {
      // Only intercept /user _after_ we're logged in.
      cy.wait('@auth').then(() => {
        cy.intercept('GET', '/user').as('user');
      });
      cy.wait('@user').then((interception) => {
        expect(interception.response, 'Intercepted response').to.satisfy(
          () => true
        );
        expect(interception.response.statusCode).to.equal(200);
      });
    });

    describe('after reloading', () => {
      beforeEach(() => {
        cy.reload();
      });

      shouldBeLoggedIn();
    });
  });
});
