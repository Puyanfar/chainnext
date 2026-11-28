describe('OAuth Auth Error UX (#1273)', () => {
  describe('OAuth callback failure paths redirect instead of returning raw JSON', () => {
    it('redirects on provider-returned error param', () => {
      cy.request({
        url: '/auth/oauth/github/callback?error=access_denied',
        followRedirect: false,
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.equal(302);
        expect(response.headers['location']).to.include(
          '/login?error=oauthSignin'
        );
      });
    });

    it('redirects on invalid state (no raw JSON 401) — regression for #1273', () => {
      cy.request({
        url: '/auth/oauth/github/callback?code=fake_code&state=fake_state',
        followRedirect: false,
        failOnStatusCode: false
      }).then((response) => {
        expect(response.status).to.equal(302);
        expect(response.headers['location']).to.include(
          '/login?error=oauthSignin'
        );
        expect(response.headers['content-type'] || '').to.not.include(
          'application/json'
        );
      });
    });
  });

  describe('login page renders friendly OAuth error message', () => {
    it('shows a specific message for oauthSignin error', () => {
      cy.visit('/login');
      // Cypress 16 rewrites the query string on cy.visit (injects its own
      // browser-detection params), so set the error param via client-side
      // navigation instead to make sure the SPA picks it up.
      cy.window().then((win) => {
        win.history.replaceState({}, '', '/login?error=oauthSignin');
        win.dispatchEvent(new win.PopStateEvent('popstate'));
      });
      cy.get('[role="alert"]').should(
        'contain',
        'Sign in failed. Please try again, or use a different sign-in method.'
      );
      cy.get('body').should('not.contain', '{"detail"');
    });
  });
});
