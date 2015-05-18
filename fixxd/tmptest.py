from fixxd import core

try:
    core.test("MyApp.app", "~/devel/automation/ReplayUITest.js")
except Exception as e:
    print "Error {0}".format(e)
