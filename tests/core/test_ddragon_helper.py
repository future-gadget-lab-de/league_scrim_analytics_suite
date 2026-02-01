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


# Helper-Funktion: Startet alle Patches und gibt die Mocks + Cleanup zurück.
# Vorteil: Kein Contextmanager nötig, aber trotzdem wenig Wiederholung.
def start_ddragon_mocks(
    *,
    read_json=None,
    request_json=None,
    today=None,
):
    # Standardwerte, falls der Test nichts Spezifisches übergibt.
    read_json = {} if read_json is None else read_json
    request_json = {"v": "0.0.0"} if request_json is None else request_json
    today = real_datetime(2025, 1, 2) if today is None else today

    patchers = [
        mock.patch.object(ddragon.config, "general_settings", new=TEST_SETTINGS),
        mock.patch.object(ddragon, "readJsonFile", return_value=read_json),
        mock.patch.object(ddragon, "requestJsonFile", return_value=request_json),
        mock.patch.object(ddragon.datetime, "datetime"),
    ]

    mocks = [p.start() for p in patchers]

    # datetime.today() soll immer ein festes Datum liefern.
    mocks[5].today.return_value = today

    # Cleanup-Funktion, die alle Patches wieder stoppt.
    def cleanup():
        for p in patchers:
            p.stop()

    return {
        "read_json": mocks[1],
        "request_json": mocks[2],
        "mock_dt": mocks[3],
        "cleanup": cleanup,
    }


class TestDDragonWithHelperFunction(unittest.TestCase):
    def test_returnScrapeLink_with_patch_does_not_scrape(self):
        # Helper starten und sicher wieder stoppen (finally).
        m = start_ddragon_mocks()
        try:
            with mock.patch.object(ddragon, "scrapeRecentPatch") as scrape_patch:
                link = ddragon.returnScrapeLink("item", "14.1.0")

            # Erwarteter Link mit dem übergebenen Patch.
            self.assertEqual(
                link,
                "https://ddragon.leagueoflegends.com/cdn/14.1.0/data/en_US/item.json",
            )
            # Sicherstellen: scrapeRecentPatch wurde nicht verwendet.
            scrape_patch.assert_not_called()
        finally:
            m["cleanup"]()

    def test_returnScrapeLink_without_patch_uses_scrape(self):
        m = start_ddragon_mocks()
        try:
            with mock.patch.object(ddragon, "scrapeRecentPatch", return_value="14.2.0") as scrape_patch:
                link = ddragon.returnScrapeLink("champion")

            # Der Link muss den gemockten Patch enthalten.
            self.assertEqual(
                link,
                "https://ddragon.leagueoflegends.com/cdn/14.2.0/data/en_US/champion.json",
            )
            # Sicherstellen: scrapeRecentPatch wurde genau einmal genutzt.
            scrape_patch.assert_called_once()
        finally:
            m["cleanup"]()

    def test_loadIdDataSet_uses_cache(self):
        m = start_ddragon_mocks(read_json={"ok": True})
        try:
            data = ddragon.loadIdDataSet("summoner", "14.1.0")

            # Die Funktion soll die gecachten Daten zurückgeben.
            self.assertEqual(data, {"ok": True})
            # Prüfen, dass der erwartete Pfad zum Cache verwendet wurde.
            m["read_json"].assert_called_once_with(
                "meta_test/prof1/dictionaries/summoner_14.1.0.json"
            )
            # requestJsonFile darf NICHT aufgerufen werden, da Cache vorhanden ist.
            m["request_json"].assert_not_called()
        finally:
            m["cleanup"]()

    def test_loadIdDataSet_cache_miss_requests(self):
        m = start_ddragon_mocks(read_json={}, request_json={"data": 1})
        try:
            with mock.patch.object(ddragon, "returnScrapeLink", return_value="http://example") as scrape_link:
                data = ddragon.loadIdDataSet("perk", "14.1.0")

            # Die Funktion soll die geladenen Daten zurückgeben.
            self.assertEqual(data, {"data": 1})
            # Erneut: Cache-Pfad muss stimmen.
            m["read_json"].assert_called_once_with(
                "meta_test/prof1/dictionaries/perk_14.1.0.json"
            )
            # returnScrapeLink wurde verwendet, um die URL zu bauen.
            scrape_link.assert_called_once_with("perk", "14.1.0")
            # requestJsonFile muss mit URL und Save-Path aufgerufen werden.
            m["request_json"].assert_called_once_with(
                "http://example",
                saveLocation="meta_test/prof1/dictionaries/perk_14.1.0.json",
            )
        finally:
            m["cleanup"]()

    def test_scrapeRecentPatch_cache_miss_requests(self):
        m = start_ddragon_mocks(read_json={}, request_json={"v": "14.2.1"})
        try:
            patch = ddragon.scrapeRecentPatch()

            # Die Version aus dem JSON muss zurückgegeben werden.
            self.assertEqual(patch, "14.2.1")
            # Der Pfad soll das Datum aus dem Mock enthalten.
            m["read_json"].assert_called_once_with(
                "meta_test/prof1/dictionaries/EUW_2025-01-02.json"
            )
            # Request muss mit korrekter URL und Save-Path passieren.
            m["request_json"].assert_called_once_with(
                "https://ddragon.leagueoflegends.com/realms/euw.json",
                saveLocation="meta_test/prof1/dictionaries/EUW_2025-01-02.json",
            )
        finally:
            m["cleanup"]()
