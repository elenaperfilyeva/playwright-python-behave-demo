from playwright.sync_api import sync_playwright
import configparser
import allure
from pathlib import Path
from behave.contrib.scenario_autoretry import patch_scenario_with_autoretry


def read_config():
    config = configparser.ConfigParser()
    config.read('behave.ini')
    return config


def get_base_url():
    config = read_config()
    base_url = config.get('env', 'base_url')
    return base_url


def add_environment_info_to_allure_report(context):
    config = read_config()
    allure_dir = config.get('behave', 'outfiles')
    base_url = get_base_url()
    if allure_dir:
        with open(f'{allure_dir}/environment.properties', 'w') as file:
            file.write(f'base_url={base_url}\n')


def attach_screenshot_to_allure_report(context, attachment_name):
    screenshot_dir = Path('screenshots')
    screenshot_dir.mkdir(exist_ok=True)
    context.page.screenshot(path=str(screenshot_dir / f'{attachment_name}.png'), full_page=True)
    allure.attach(
        context.page.screenshot(type='png'),
        name=f'screenshot_{attachment_name}.png',
        attachment_type=allure.attachment_type.PNG
    )


def attach_video_to_allure_report(context, attachment_name):
    video_path = context.page.video.path()
    context.page.context.close()        # to save video
    allure.attach.file(
        video_path,
        name=f'video_{attachment_name}.webm',
        attachment_type=allure.attachment_type.WEBM
    )


def before_all(context):
    context.playwright = sync_playwright().start()
    headless = True
    if 'headed' in context.config.userdata:
        headless = False
    context.browser = context.playwright.chromium.launch(headless=headless)
    add_environment_info_to_allure_report(context)


def before_feature(context, feature):
    for scenario in feature.scenarios:
        if 'wip' not in scenario.tags:
            patch_scenario_with_autoretry(scenario, max_attempts=3)


def before_scenario(context, scenario):
    context.context = context.browser.new_context(ignore_https_errors=True, record_video_dir='videos')
    context.page = context.context.new_page()
    base_url = get_base_url()
    context.page.goto(base_url)


def after_step(context, step):
    if step.status == 'failed':
        attachment_name = context.scenario.name.replace(' ', '_').replace('.', '_').replace('@', '').lower()
        attach_screenshot_to_allure_report(context,attachment_name)
        attach_video_to_allure_report(context, attachment_name)


def after_scenario(context,scenario):
    if hasattr(context, 'page'):
        context.page.close()
        context.context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
