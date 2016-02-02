from noseapp_requests import make_config, RequestsEx
from noseapp import Suite
from noseapp import NoseApp
from noseapp.case import step
from noseapp import ScreenPlayCase
import random, string

class TestApplication(NoseApp):

    def initialization(self):
        self.settings_setup()

    def settings_setup(self):
        endpoint = make_config()
        endpoint.configure(
            base_url = "http://127.0.0.1:5000",
            key = "localhost"
        )
        requests_ex = RequestsEx(endpoint)
        global api
        api = requests_ex.get_endpoint_session('localhost')

def create_TestApplication(config=None, argv=None, plugins=None):
    return TestApplication(config=config,argv=argv,plugins=plugins)

suite = Suite(__name__)

@suite.register
class TestPost(ScreenPlayCase):

    def random_word(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(8))

    def generate(self):
        date = api.get("dictionary").json()
        self.test_key = self.random_word()
        while self.test_key in date.keys():
            self.test_key = self.random_word()

    @step(1,"POST without value")
    def one_step(self):
        assert api.post("dictionary",{"key":self.test_key,"value":"Hello World!"}).status_code == 409

    @step(2,"POST dont have a key")
    def two_step(self):
        assert api.post("dictionaty",{"value":self.test_key}).status_code == 400

    @step(3,"POST dont have a value")
    def three_step(self):
        assert api.post("dictionaty",{"key":self.test_key}).status_code == 400

@suite.register
class TestGet(ScreenPlayCase):
    def random_word(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(8))

    def generate(self):
        date = api.get("dictionary").json()
        self.test_key = self.random_word()
        while self.test_key in date.keys():
            self.test_key = self.random_word()

        @step(1,"key exists in date ")
        def one_step(self):
            assert api.get("dictionary/" + self.test_key).status_code == 404

@suite.register
class TestPut():
    def random_word(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(8))

    def __init__(self):
        date = api.get("dictionary").json()
        self.test_key = self.random_word()
        while self.test_key in date.keys():
            self.test_key = self.random_word()

    @step(1,"key not in date")
    def test(self):
        assert api.put("dictionary" + self.test_key,{"test":"test"}).status_code == 404

@suite.register
class TestDelete(ScreenPlayCase):
    def random_word(self):
        return "".join(random.choice(string.ascii_lowercase) for i in range(8))

    def generate(self):
        date = api.get("dictionary").json()
        self.test_key = self.random_word()
        while self.test_key in date.keys():
            self.test_key = self.random_word()
        api.post("dictionary",{"key":self.test_key,"value":self.test_key})

        @step(1,"key not in date")
        def test_delete(self):
            result = api.delete("dictionary/"+self.test_key).join()
            assert "result" in result.keys()

app = create_TestApplication()
app.register_suite(suite)
app.run()







