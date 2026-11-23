describe('plotly', () => {
  it('should be able to display an inline chart', () => {
    cy.get('.step').should('have.length', 1);
    cy.get('.step').eq(0).find('.inline-plotly').should('have.length', 1);
    cy.get('.step').eq(0).find('.inline-plotly .main-svg').should('exist');
    cy.get('.step')
      .eq(0)
      .find('.inline-plotly .barlayer .point')
      .should('have.length', 3);
  });
});
