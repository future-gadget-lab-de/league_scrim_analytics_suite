import unittest
from datetime import datetime as real_datetime
from unittest import mock

from src.core.apis import ddragon
from src.core.config import Configs

# Minimale Konfiguration, die die Tests brauchen, damit Pfade berechnet werden können.
TEST_SETTINGS = {
    Configs.MAIN: {
        "metadata_directory": "meta_test",
        "current_prof": "prof1",
    }
}


class TestDDragonWithSetUpTearDown(unittest.TestCase):
    # setUp wird vor jedem Test ausgeführt.
    # Wir starten hier alle Patches, damit jeder Test die gleichen "Fake"-Abhängigkeiten hat.
    def setUp(self):
        self.read_json_value = {}
        self.request_json_value = {"v": "0.0.0"}
        self.scrape_link_value = "http://example"
        self.today_value = real_datetime(2025, 1, 2)

        # Patchers speichern wir, um sie in tearDown sauber zu stoppen.
        self.patchers = [
            mock.patch.object(ddragon.config, "general_settings", new=TEST_SETTINGS),
            mock.patch.object(ddragon, "readJsonFile", return_value=self.read_json_value),
            mock.patch.object(ddragon, "requestJsonFile", return_value=self.request_json_value),
            mock.patch.object(ddragon.datetime, "datetime"),
        ]

        # Patches aktivieren und Mocks speichern.
        self.mocks = [p.start() for p in self.patchers]

        # Mocks sauber benennen, damit die Tests lesbar sind.
        self.mock_read_json = self.mocks[1]
        self.mock_request_json = self.mocks[2]
        self.mock_dt = self.mocks[3]

        # datetime.today() soll immer ein festes Datum liefern.
        self.mock_dt.today.return_value = self.today_value

    # tearDown wird nach jedem Test ausgeführt.
    # Hier stoppen wir alle Patches wieder, damit nichts "hängen bleibt".
    def tearDown(self):
        for p in self.patchers:
            p.stop()

    def test_returnScrapeLink_with_patch_does_not_scrape(self):
        # Wenn ein Patch explizit übergeben wird, soll scrapeRecentPatch NICHT aufgerufen werden.
        with mock.patch.object(ddragon, "scrapeRecentPatch") as scrape_patch:
            link = ddragon.returnScrapeLink("item", "14.1.0")

        # Erwarteter Link mit dem übergebenen Patch.
        self.assertEqual(
            link,
            "https://ddragon.leagueoflegends.com/cdn/14.1.0/data/en_US/item.json",
        )
        # Sicherstellen: scrapeRecentPatch wurde nicht verwendet.
        scrape_patch.assert_not_called()

    def test_returnScrapeLink_without_patch_uses_scrape(self):
        # Wenn kein Patch übergeben wird, soll scrapeRecentPatch den Patch liefern.
        with mock.patch.object(ddragon, "scrapeRecentPatch", return_value="14.2.0") as scrape_patch:
            link = ddragon.returnScrapeLink("champion")

        # Der Link muss den gemockten Patch enthalten.
        self.assertEqual(
            link,
            "https://ddragon.leagueoflegends.com/cdn/14.2.0/data/en_US/champion.json",
        )
        # Sicherstellen: scrapeRecentPatch wurde genau einmal genutzt.
        scrape_patch.assert_called_once()

    def test_loadIdDataSet_uses_cache(self):
        # readJsonFile liefert Daten -> es sollte kein HTTP-Request passieren.
        self.mock_read_json.return_value = {"ok": True}
        data = ddragon.loadIdDataSet("summoner", "14.1.0")

        # Die Funktion soll die gecachten Daten zurückgeben.
        self.assertEqual(data, {"ok": True})
        # Prüfen, dass der erwartete Pfad zum Cache verwendet wurde.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/summoner_14.1.0.json"
        )
        # requestJsonFile darf NICHT aufgerufen werden, da Cache vorhanden ist.
        self.mock_request_json.assert_not_called()

    def test_loadIdDataSet_cache_miss_requests(self):
        # readJsonFile liefert leeres Dict -> es muss von der API geholt werden.
        self.mock_read_json.return_value = {}
        self.mock_request_json.return_value = {"data": 1}
        with mock.patch.object(ddragon, "returnScrapeLink", return_value="http://example") as scrape_link:
            data = ddragon.loadIdDataSet("perk", "14.1.0")

        # Die Funktion soll die geladenen Daten zurückgeben.
        self.assertEqual(data, {"data": 1})
        # Erneut: Cache-Pfad muss stimmen.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/perk_14.1.0.json"
        )
        # returnScrapeLink wurde verwendet, um die URL zu bauen.
        scrape_link.assert_called_once_with("perk", "14.1.0")
        # requestJsonFile muss mit URL und Save-Path aufgerufen werden.
        self.mock_request_json.assert_called_once_with(
            "http://example",
            saveLocation="meta_test/prof1/dictionaries/perk_14.1.0.json",
        )

    def test_scrapeRecentPatch_cache_miss_requests(self):
        # Wenn es keine lokale Datei gibt, soll die Funktion einen Request ausführen.
        self.mock_read_json.return_value = {}
        self.mock_request_json.return_value = {"v": "14.2.1"}
        patch = ddragon.scrapeRecentPatch()

        # Die Version aus dem JSON muss zurückgegeben werden.
        self.assertEqual(patch, "14.2.1")
        # Der Pfad soll das Datum aus dem Mock enthalten.
        self.mock_read_json.assert_called_once_with(
            "meta_test/prof1/dictionaries/EUW_2025-01-02.json"
        )
        # Request muss mit korrekter URL und Save-Path passieren.
        self.mock_request_json.assert_called_once_with(
            "https://ddragon.leagueoflegends.com/realms/euw.json",
            saveLocation="meta_test/prof1/dictionaries/EUW_2025-01-02.json",
        )
