# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from medialog.docenttheme.testing import MEDIALOG_DOCENTTHEME_INTEGRATION_TESTING  # noqa: E501

import unittest


try:
    from Products.CMFPlone.utils import get_installer
except ImportError:
    get_installer = None


class TestSetup(unittest.TestCase):
    """Test that medialog.docenttheme is properly installed."""

    layer = MEDIALOG_DOCENTTHEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if medialog.docenttheme is installed."""
        self.assertTrue(self.installer.is_product_installed(
            'medialog.docenttheme'))

    def test_browserlayer(self):
        """Test that IMedialogDocentthemeLayer is registered."""
        from medialog.docenttheme.interfaces import (
            IMedialogDocentthemeLayer)
        from plone.browserlayer import utils
        self.assertIn(
            IMedialogDocentthemeLayer,
            utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = MEDIALOG_DOCENTTHEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        if get_installer:
            self.installer = get_installer(self.portal, self.layer['request'])
        else:
            self.installer = api.portal.get_tool('portal_quickinstaller')
        roles_before = api.user.get_roles(TEST_USER_ID)
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.installer.uninstall_product('medialog.docenttheme')
        setRoles(self.portal, TEST_USER_ID, roles_before)

    def test_product_uninstalled(self):
        """Test if medialog.docenttheme is cleanly uninstalled."""
        self.assertFalse(self.installer.is_product_installed(
            'medialog.docenttheme'))

    def test_browserlayer_removed(self):
        """Test that IMedialogDocentthemeLayer is removed."""
        from medialog.docenttheme.interfaces import \
            IMedialogDocentthemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IMedialogDocentthemeLayer, utils.registered_layers())
