Feature: Account registry

  Scenario: User is able to create 2 accounts
    Given Account registry is empty
    When I create an account using name: "kurt", last name: "cobain", pesel: "89092909246"
    And I create an account using name: "tadeusz", last name: "szcześniak", pesel: "79101011234"
    Then Number of accounts in registry equals: "2"
    And Account with pesel "89092909246" exists in registry
    And Account with pesel "79101011234" exists in registry

  Scenario: User is able to update surname of already created account
    Given Account registry is empty
    And I create an account using name: "nata", last name: "haydamaky", pesel: "95092909876"
    When I update "surname" of account with pesel: "95092909876" to "filatov"
    Then Account with pesel "95092909876" has "surname" equal to "filatov"

  Scenario: User is able to update name of already created account
    Given Account registry is empty
    And I create an account using name: "anna", last name: "kowalska", pesel: "88010112345"
    When I update "name" of account with pesel: "88010112345" to "anna-maria"
    Then Account with pesel "88010112345" has "name" equal to "anna-maria"

  Scenario: Created account has all fields correctly set
    Given Account registry is empty
    When I create an account using name: "michal", last name: "kowal", pesel: "70010100001"
    Then Account with pesel "70010100001" exists in registry
    And Number of accounts in registry equals: "1"

  Scenario: User is able to delete created account
    Given Account registry is empty
    And I create an account using name: "parov", last name: "stelar", pesel: "01092909876"
    When I delete account with pesel: "01092909876"
    Then Account with pesel "01092909876" does not exist in registry
    And Number of accounts in registry equals: "0"

  Scenario: User can perform incoming transfers and balance updates
    Given Account registry is empty
    And I create an account using name: "payer", last name: "one", pesel: "11111111111"
    When I perform an incoming transfer of 100 to account with pesel: "11111111111"
    And I perform an incoming transfer of 50 to account with pesel: "11111111111"
    Then Account with pesel "11111111111" has "balance" equal to "150"
