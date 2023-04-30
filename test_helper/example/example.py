from test_helper import Test

x = 1
y = 2

Test.assertEquals(x, 1)
Test.assertEquals(x + 1, 2)
Test.assertEquals(y, 1, "y is incorrect")

Test.assertEqualsHashed(x,'356a192b7913b04c54574d18c28d46e6395428ab', 'this is a test')

Test.printStats()

Test.setFailFast()
Test.setPrivateMode()
Test.assertEquals(y, 1, "y is incorrect")
