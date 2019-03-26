# -*- coding: utf-8 -*-
#
# Copyright (C) 2015-2019 Bitergia
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Valerio Cosentino <valcos@bitergia.com>
#

import logging
import unittest

from base import TestBaseBackend


class TestFinosMeetings(TestBaseBackend):
    """Test FinosMeetings backend"""

    connector = "finosmeetings"
    ocean_index = "test_" + connector
    enrich_index = "test_" + connector + "_enrich"

    def test_has_identites(self):
        """Test value of has_identities method"""

        enrich_backend = self.connectors[self.connector][2]()
        self.assertTrue(enrich_backend.has_identities())

    def test_items_to_raw(self):
        """Test whether JSON items are properly inserted into ES"""

        result = self._test_items_to_raw()
        self.assertEqual(result['items'], 3)
        self.assertEqual(result['raw'], 3)

    def test_raw_to_enrich(self):
        """Test whether the raw index is properly enriched"""

        result = self._test_raw_to_enrich()
        self.assertEqual(result['raw'], 3)
        self.assertEqual(result['enrich'], 3)

        enrich_backend = self.connectors[self.connector][2]()

        item = self.items[0]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('csv_org', eitem)
        self.assertNotIn('org', eitem)
        self.assertNotIn('project', eitem)

        item = self.items[1]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('csv_org', eitem)
        self.assertNotIn('org', eitem)
        self.assertNotIn('project', eitem)

        item = self.items[2]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('csv_org', eitem)
        self.assertNotIn('org', eitem)
        self.assertNotIn('project', eitem)

    def test_raw_to_enrich_sorting_hat(self):
        """Test enrich with SortingHat"""

        result = self._test_raw_to_enrich(sortinghat=True)
        self.assertEqual(result['raw'], 3)
        self.assertEqual(result['enrich'], 3)

        enrich_backend = self.connectors[self.connector][2]()
        enrich_backend.sortinghat = True

        item = self.items[0]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('author_id', eitem)
        self.assertIn('author_uuid', eitem)
        self.assertIn('author_name', eitem)
        self.assertIn('author_user_name', eitem)
        self.assertIn('email_uuid', eitem)
        self.assertIn('email_name', eitem)
        self.assertIn('email_user_name', eitem)

        item = self.items[1]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('author_id', eitem)
        self.assertIn('author_uuid', eitem)
        self.assertIn('author_name', eitem)
        self.assertIn('author_user_name', eitem)
        self.assertIn('email_uuid', eitem)
        self.assertIn('email_name', eitem)
        self.assertIn('email_user_name', eitem)

        item = self.items[2]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('author_id', eitem)
        self.assertIn('author_uuid', eitem)
        self.assertIn('author_name', eitem)
        self.assertIn('author_user_name', eitem)
        self.assertIn('email_uuid', eitem)
        self.assertIn('email_name', eitem)
        self.assertIn('email_user_name', eitem)

    def test_raw_to_enrich_projects(self):
        """Test enrich with Projects"""

        result = self._test_raw_to_enrich(projects=True)
        self.assertEqual(result['raw'], 3)
        self.assertEqual(result['enrich'], 3)

        enrich_backend = self.connectors[self.connector][2]()
        enrich_backend.prjs_map = True

        item = self.items[0]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('project', eitem)
        self.assertEqual(eitem['project'], eitem['cm_program'])
        self.assertEqual(eitem['project_1'], eitem['cm_program'])

        item = self.items[1]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('project', eitem)
        self.assertEqual(eitem['project'], eitem['cm_program'])
        self.assertEqual(eitem['project_1'], eitem['cm_program'])

        item = self.items[2]
        eitem = enrich_backend.get_rich_item(item)
        self.assertIn('project', eitem)
        self.assertEqual(eitem['project'], eitem['cm_program'])
        self.assertEqual(eitem['project_1'], eitem['cm_program'])

    def test_refresh_identities(self):
        """Test refresh identities"""

        result = self._test_refresh_identities()
        # ... ?

    def test_refresh_project(self):
        """Test refresh project field for all sources"""

        result = self._test_refresh_project()
        # ... ?


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    unittest.main(warnings='ignore')
