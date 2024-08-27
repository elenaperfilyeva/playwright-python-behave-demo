import random
from behave import *


# STEP FOR DEBUGGING
# DON'T USE IT FOR ANY OTHER PURPOSES
@given("STOP HERE AND OPEN PLAYWRIGHT INSPECTOR")
def step_impl(context):
    context.page.pause()


# STEP FOR TEST REPORT DEBUGGING ONLY
# DON'T USE IT FOR ANY OTHER PURPOSES
@given("BREAK THE TEST")
def step_impl(context):
    assert False, "THE TEST BROKEN TO DEBUG TEST RESULTS"


# STEP FOR TEST REPORT DEBUGGING ONLY
# DON'T USE IT FOR ANY OTHER PURPOSES
@given("MAKE THE TEST FLAKY")
def step_impl(context):
    assert random.choice([True, False]), "BAD LUCK FLAKY TEST"



