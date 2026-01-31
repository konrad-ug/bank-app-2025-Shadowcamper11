const { expect } = require('@playwright/test');

class EmployeesPage {
  constructor(page) {
    this.page = page;
  }

  async searchEmployee(name) {
    await this.page.getByLabel('Imię lub nazwisko').fill(name);
  }

  async openEmployee(fullName) {
    const employeeLink = this.page.getByRole('link', { name: fullName });
    await expect(employeeLink).toBeVisible();
    await employeeLink.click();
  }

  async checkRoomNumber(room) {
    await expect(this.page.getByText(`Nr pokoju: ${room}`)).toBeVisible();
  }
}

module.exports = { EmployeesPage };
