import unittest
from unittest import mock

from src.core.config import Configs
from src.core.apis import riot

MINIMAL_TEST_CONFIG = {
    Configs.MAIN: {
        "API_key": "urf",
    }
}     

class TestRiotApiLink(unittest.TestCase):
    def setUp(self):
        self.request_value = {"puuid": "42"}

        self.config_patcher = mock.patch.object(
            riot.config, "general_settings", new=MINIMAL_TEST_CONFIG
        )
        self.request_patcher = mock.patch.object(
            riot, "requestJsonFile", return_value=self.request_value
        )

        self.config_patcher.start()
        self.request_mock = self.request_patcher.start()

    def _auth_headers(self):
        return {
            "X-Riot-Token": MINIMAL_TEST_CONFIG[Configs.MAIN]["API_key"],
            "Accept": "application/json",
            "User-Agent": "my-riot-client/1.0",
        }

    def tearDown(self):
        self.request_patcher.stop()
        self.config_patcher.stop()

    def test_getPUIDbySummAndTag_result(self):
        puuid = riot.getPUIDbySummAndTagline("Faker", "EUW")
        self.assertEqual(puuid, self.request_value["puuid"])

    def test_getPUIDbySummAAndTag_link_validity(self):
        puuid = riot.getPUIDbySummAndTagline("Faker", "EUW")
        self.request_mock.assert_called_once_with(
            f"https://europe.api.riotgames.com/riot/account/v1/accounts/" + \
                f"by-riot-id/Faker/EUW?api_key={MINIMAL_TEST_CONFIG[Configs.MAIN]['API_key']}"
        )

    def test_getSummonerSample_with_wrong_args(self):
        with self.assertRaises(ValueError):
            userlist = riot.getSummonerSample("WOOD", "RANKED_SOLO_5x5", "I", 1)
        with self.assertRaises(TypeError):
            userlist = riot.getSummonerSample("GOLD", "RANKED_SOLO_5x5", "I", -3)

    def test_getSummonerSample_link_validity(self):
        userlist = riot.getSummonerSample("GOLD", "RANKED_SOLO_5x5", "I", 2)
        self.request_mock.assert_called_once_with(
            f"https://euw1.api.riotgames.com/lol/league-exp/v4/entries/" + \
                f"RANKED_SOLO_5x5/GOLD/I?page=2",
            self._auth_headers()
        )

    def test_getSummonerSample_result(self):
        self.request_mock.return_value = ["besenstiel"]
        userlist = riot.getSummonerSample("GOLD", "RANKED_SOLO_5x5", "I", 2)
        self.assertListEqual(userlist, ["besenstiel"])

    def test_getGameIdsByPuuid_result(self):
        self.request_mock.return_value = ["die lösung"]
        userdata = riot.getGameIdsByPuuid("42")
        self.assertListEqual(userdata, ["die lösung"])

    def test_getGameIdsByPuuid_link_validity(self):
        userlist = riot.getGameIdsByPuuid("42")
        self.request_mock.assert_called_once_with(
            f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/" + \
                f"42/ids?type=ranked&start=0&count=100",
            self._auth_headers()
        )

    #def test_getGameById_result(self):
     #   matchdicts = riot.getGameById("")
