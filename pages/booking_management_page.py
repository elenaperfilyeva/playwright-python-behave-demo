from playwright.sync_api import Page


class BookingManagementPage(Page):
    def __init__(self, page: Page):
        self.page = page