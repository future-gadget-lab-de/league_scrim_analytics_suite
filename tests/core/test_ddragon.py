import unittest
from datetime import datetime as real_datetime
from unittest import mock

from src.core.apis import ddragon
from src.core.config import Configs

# Minimal configuration the tests need so paths can be computed.
TEST_SETTINGS = {
    Configs.MAIN: {
        "metadata_directory": "meta_test",
        "current_prof": "prof1",
    }
}


class TestDDragon(unittest.TestCase):
    # setUp runs before each test.
    # We start all patches here so every test has the same "fake" dependencies.
    def setUp(self):
        self.read_json_value = {}
        self.request_json_value = {"v": "0.0.0"}
        self.scrape_link_value = "http://example"
        self.today_value = real_datetime(2025, 1, 2)

        # We store patchers to stop them cleanly in tearDown.
        self.patchers = [
            mock.patch.object(ddragon.config, "general_settings", new=TEST_SETTINGS),
            mock.patch.object(ddragon, "readJsonFile", return_value=self.read_json_value),
            mock.patch.object(ddragon, "requestJsonFile", return_value=self.request_json_value),
            mock.patch.object(ddragon.datetime, "datetime"),
        ]

        # Activate patches and store mocks.
        self.mocks = [p.start() for p in self.patchers]

        # Name mocks clearly to keep tests readable.
        self.mock_read_json = self.mocks[1]
        self.mock_request_json = self.mocks[2]
        self.mock_dt = self.mocks[3]

        # datetime.today() should always return a fixed date.
        self.mock_dt.today.return_value = self.today_value

    # tearDown runs after each test.
    # We stop all patches here so nothing "sticks" around.
    def tearDown(self):
        for p in self.patchers:
            p.stop()

    def test_returnScrapeLink_with_patch_does_not_scrape(self):
        # If a patch is explicitly provided, scrapeRecentPatch should NOT be called.
        with mock.patch.object(ddragon, "scrapeRecentPatch") as scrape_patch:
            link = ddragon.returnScrapeLink("item", "14.1.0")

        # Expected link with the provided patch.
        self.assertEqual(
            link,
            "https://ddragon.leagueoflegends.com/cdn/14.1.0/data/en_US/item.json",
        )
        # Ensure scrapeRecentPatch was not used.
        scrape_patch.assert_not_called()

    def test_returnScrapeLink_without_patch_uses_scrape(self):
        # If no patch is provided, scrapeRecentPatch should supply it.
        with mock.patch.object(ddragon, "scrapeRecentPatch", return_value="14.2.0") as scrape_patch:
            link = ddragon.returnScrapeLink("champion")

        # The link must contain the mocked patch.
        self.assertEqual(
            link,
            "https://ddragon.leagueoflegends.com/cdn/14.2.0/data/en_US/champion.json",
        )
        # Ensure scrapeRecentPatch was used exactly once.
        scrape_patch.assert_called_once()

    def test_loadIdDataSet_uses_cache(self):
        # readJsonFile returns data -> no HTTP request should happen.
        self.mock_read_json.return_value = {"ok": True}
        data = ddragon.loadIdDataSet("summoner", "14.1.0")

        # The function should return the cached data.
        self.assertEqual(data, {"ok": True})
        # Verify the expected cache path was used.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/summoner_14.1.0.json"
        )
        # requestJsonFile must NOT be called since cache is present.
        self.mock_request_json.assert_not_called()

    def test_loadIdDataSet_cache_miss_requests(self):
        # readJsonFile returns an empty dict -> it must be fetched from the API.
        self.mock_read_json.return_value = {}
        self.mock_request_json.return_value = {"data": 1}
        with mock.patch.object(ddragon, "returnScrapeLink", return_value="http://example") as scrape_link:
            data = ddragon.loadIdDataSet("perk", "14.1.0")
        # The function should return the fetched data.
        self.assertEqual(data, {"data": 1})
        # Again: cache path must be correct.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/perk_14.1.0.json"
        )
        # returnScrapeLink was used to build the URL.
        scrape_link.assert_called_once_with("perk", "14.1.0")
        # requestJsonFile must be called with URL and save path.
        self.mock_request_json.assert_called_once_with(
            "http://example",
            saveLocation="meta_test/prof1/dictionaries/perk_14.1.0.json",
        )

    def test_scrapeRecentPatch_cache_miss_requests(self):
        # If there is no local file, the function should make a request.
        self.mock_read_json.return_value = {}
        self.mock_request_json.return_value = {"v": "14.2.1"}
        patch = ddragon.scrapeRecentPatch()

        # The version from the JSON must be returned.
        self.assertEqual(patch, "14.2.1")
        # The path should include the date from the mock.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/EUW_2025-01-02.json"
        )
        # The request must use the correct URL and save path.
        self.mock_request_json.assert_called_once_with(
            "https://ddragon.leagueoflegends.com/realms/euw.json",
            saveLocation="meta_test/prof1/dictionaries/EUW_2025-01-02.json",
        )

    def test_loadIdDataSet_wrong_argument(self):

        self.mock_read_json.return_value = {}
        
        with self.assertRaises(ValueError):
            data_dict = ddragon.loadIdDataSet("regenbogen", "14.2.1")

        self.mock_request_json.assert_not_called()
