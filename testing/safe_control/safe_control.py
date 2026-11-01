#Testing how the logic in my control loop might look like

class TestNetwork:

    def __init__(self):
        self.prb = 50

    def get_config(self):
        return self.prb

    def change_config(self, new_prb):
        self.prb = new_prb

class TestController:

    def __init__(self, network):
        self.network = network
        self.min_prb = 10
        self.max_prb = 70
        self.safe_config = None

    def validator(self, new_prb):
        return(isinstance(new_prb, int) and self.min_prb <= new_prb <= self.max_prb)

    def attempt_change(self, new_prb):
        if not self.validator(new_prb):
            return False

        self.safe_config = self.network.get_config()

        self.network.change_config(new_prb)

        new_config = self.network.get_config()

        if new_prb == new_config:
            return "change successful"
        else:
            return "change unsuccesful"

    def rollback(self):
        if self.safe_config == None:
            return "No safe configuration available"

        self.network.change_config(self.safe_config)

        current_config = self.network.get_config()

        if current_config == self.safe_config:
            return "Successful rollback"
        else:
            return "Unsuccessfu; rollback"

        
        