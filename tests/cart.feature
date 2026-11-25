Feature: Shopping cart
  Scenario: Add the same product twice
    Given an empty cart
    When I add a ten dollar product twice
    Then the cart quantity is 2
    And the grand total is 32 dollars
  Scenario: Remove the last item
    Given a cart with one product
    When I decrease its quantity
    Then the cart quantity is 0
