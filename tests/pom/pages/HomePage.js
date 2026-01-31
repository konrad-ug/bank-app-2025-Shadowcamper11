class HomePage {
  constructor(page) {
    this.page = page;
    this.header = page.locator('header');
  }

  async open() {
    await this.page.goto('https://mfi.ug.edu.pl/');
  }

  async goToEmployees() {
    await this.header.getByRole('link', { name: 'Pracownicy' }).hover();
    await this.header.getByRole('link', { name: 'Skład osobowy' }).click();
  }
}

module.exports = { HomePage };
