import unittest
from cells.scrapy.common import fix_scheme, fix_relative_url


class MyTestCase(unittest.TestCase):
    def test_fix_relative_url(self):
        self.assertEqual(fix_scheme("http://localhost.com"), "http://localhost.com")
        self.assertEqual(fix_scheme("//localhost.com"), "http://localhost.com")
        self.assertEqual(fix_scheme("www.localhost.com"), "http://www.localhost.com")
        self.assertEqual(fix_scheme("/localhost.com"), "/localhost.com")

    def test(self):
        assert fix_relative_url("http://localhost.com", "http://localhost.com/aa") == "http://localhost.com/aa"
        assert fix_relative_url("http://localhost.com", "//localhost.com/bb") == "http://localhost.com/bb"

        assert fix_relative_url("http://localhost.com", "www.localhost.com") == "http://www.localhost.com"
        assert fix_relative_url(
            "http://localhost.com",
            "sub1.sub2.localhost.cn/this-is-a-longer-post-title.html"
        ) == "http://sub1.sub2.localhost.cn/this-is-a-longer-post-title.html"

        assert fix_relative_url("http://localhost.com", "/phA/phB") == "http://localhost.com/phA/phB"
        assert fix_relative_url("http://localhost.com", "./phA/phB") == "http://localhost.com/phA/phB"

        assert fix_relative_url("http://localhost.com/phA", "../phA/a.jpg") == "http://localhost.com/phA/a.jpg"
        assert fix_relative_url("http://localhost.com/phA/phB/", "../phC/phD") == "http://localhost.com/phA/phC/phD"

        assert fix_relative_url("http://domainA.com", "http://www.domainB.com") == "http://www.domainB.com"
        assert fix_relative_url("http://domainA.com", "www.domainB.com/phA") == "http://www.domainB.com/phA"
        assert fix_relative_url("http://domainA.com", "phA") == "http://domainA.com/phA"
        assert fix_relative_url("http://domainA.com", "java") == "http://domainA.com/java"


if __name__ == "__main__":
    unittest.main()
