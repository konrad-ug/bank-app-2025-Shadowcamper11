const { test } = require('@playwright/test');
const { HomePage } = require('../pages/HomePage');
const { EmployeesPage } = require('../pages/EmployeesPage');

test('Sprawdzenie pokoju pracownika – mgr Konrad Sołtys (POM)', async ({ page }) => {
  const homePage = new HomePage(page);
  const employeesPage = new EmployeesPage(page);

  await homePage.open();
  await homePage.goToEmployees();

  await employeesPage.searchEmployee('sołtys');
  await employeesPage.openEmployee('mgr Konrad Sołtys');
  await employeesPage.checkRoomNumber('4.19');
});
