const { test, expect } = require('@playwright/test');
const { HomePage } = require('../pages/HomePage');
const { EmployeesPage } = require('../pages/EmployeesPage');

test('Zadanie 3 - Instytut Fizyki Doświadczalnej ma mgr Anna Baran', async ({ page }) => {
  const home = new HomePage(page);
  const staff = new EmployeesPage(page);

  await home.open();
  await home.goToEmployees();

  await staff.searchEmployee('Baran');

  const anna = page.getByRole('link', { name: 'mgr Anna Baran' });
  await expect(anna).toBeVisible();
});
