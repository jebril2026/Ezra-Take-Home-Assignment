from pages.member_sign_in_page import MemberSignInPage
from utils.config_loaders.config import MEMBER_URL


def test_verify_setup(page):
    member_sign_in_page = MemberSignInPage(page)
    
    member_sign_in_page.open(MEMBER_URL)
    member_sign_in_page.tap_join_link()
