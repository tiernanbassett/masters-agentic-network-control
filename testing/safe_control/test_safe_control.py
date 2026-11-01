from safe_control import TestController, TestNetwork

network = TestNetwork()

controller = TestController(network)

print("config initially =", network.get_config())

result = controller.attempt_change(60)

print( "config allowed =", result)
print( "current config =", network.get_config())
print("current checkpoint =", controller.safe_config)

print("\n testing vallidator")


print("config initially =", network.get_config())

result = controller.attempt_change(95)

print( "config allowed =", result)
print( "current config =", network.get_config())
print("current checkpoint =", controller.safe_config)

print("\n testing rollback")


print("config initially =", network.get_config())

result = controller.attempt_change(70)

print( "config allowed =", result)
print( "current config =", network.get_config())
print("current checkpoint =", controller.safe_config)
print("rollback =", controller.rollback())
print("config after rollback =", network.get_config())