"""Test availability of required packages."""

import unittest
from pathlib import Path

import pkg_resources

_REQUIREMENTS_PATH = Path(__file__).parent.with_name("requirements.txt")


class TestRequirements(unittest.TestCase):
    """Test availability of required packages."""

    def test_requirements(self):
        """Test that each required package is available."""
        # Ref: https://stackoverflow.com/a/45474387/
        requirements = pkg_resources.parse_requirements(_REQUIREMENTS_PATH.open())
        for requirement in requirements:
            requirement = str(requirement).split('==')[0] # not even looking at the version
            # With subtests you can know exactly the full subset of requirements that failed, so it's frequently useful while testing. Without subtests, you only know the first failure. – Acumenus
            # https://stackoverflow.com/questions/16294819/check-if-my-python-has-all-required-packages
            #with self.subTest(requirement=requirement):
            #    pkg_resources.require(requirement)
            
            # here, if it fails i will not look any further
            pkg_resources.require(requirement)

