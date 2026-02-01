import unittest
from datetime import datetime as real_datetime
from contextlib import contextmanager
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

# Ein Contextmanager ist eine Funktion, die man mit "with ..." benutzt.
# Sie macht Setup (z.B. Mocks aktivieren) und sorgt danach automatisch für Cleanup.
# Vorteil: Weniger Wiederholung in den Tests und sichere Rücksetzung der Mocks.
@contextmanager
def ddragon_env(
    *,
    read_json=None,
    request_json=None,
    scrape_link=None,
    today=None,
):
    # Falls der Test nichts Spezifisches übergibt, nutzen wir einfache Standardwerte.
    read_json = {} if read_json is None else read_json
    request_json = {"v": "0.0.0"} if request_json is None else request_json
    scrape_link = "http://example" if scrape_link is None else scrape_link
    today = real_datetime(2025, 1, 2) if today is None else today

    # Hier werden alle Abhängigkeiten gemockt, die sonst Dateien/Netzwerk nutzen würden.
    # Die "with ...:"-Kette stellt sicher, dass am Ende alles wieder sauber ist.
    with mock.patch.object(ddragon.config, "general_settings", new=TEST_SETTINGS), \
        mock.patch.object(ddragon, "readJsonFile", return_value=read_json) as read_json_mock, \
        mock.patch.object(ddragon, "requestJsonFile", return_value=request_json) as request_json_mock, \
        mock.patch.object(ddragon.datetime, "datetime") as mock_dt:
        # datetime.today() soll immer ein festes Datum liefern.
        mock_dt.today.return_value = today
        # Wir geben die Mock-Objekte zurück, damit Tests ihre Aufrufe prüfen können.
        yield {
            "read_json": read_json_mock,
            "request_json": request_json_mock,
            "mock_dt": mock_dt,
        }

class TestDDragon(unittest.TestCase):
    def test_returnScrapeLink_with_patch_does_not_scrape(self):
        # Wenn ein Patch explizit übergeben wird, soll scrapeRecentPatch NICHT aufgerufen werden.
        with ddragon_env(), mock.patch.object(ddragon, "scrapeRecentPatch") as scrape_patch:
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
        with ddragon_env(), mock.patch.object(ddragon, "scrapeRecentPatch", return_value="14.2.0") as scrape_patch:
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
        with ddragon_env(read_json={"ok": True}) as m:
            data = ddragon.loadIdDataSet("summoner", "14.1.0")

        # Die Funktion soll die gecachten Daten zurückgeben.
        self.assertEqual(data, {"ok": True})
        # Prüfen, dass der erwartete Pfad zum Cache verwendet wurde.
        m["read_json"].assert_called_once_with(
            "meta_test/prof1/dictionaries/summoner_14.1.0.json"
        )
        # requestJsonFile darf NICHT aufgerufen werden, da Cache vorhanden ist.
        m["request_json"].assert_not_called()

    def test_loadIdDataSet_cache_miss_requests(self):
        # readJsonFile liefert leeres Dict -> es muss von der API geholt werden.
        with ddragon_env(read_json={}, request_json={"data": 1}) as m, \
            mock.patch.object(ddragon, "returnScrapeLink", return_value="http://example") as scrape_link:
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

    def test_scrapeRecentPatch_cache_miss_requests(self):
        # Wenn es keine lokale Datei gibt, soll die Funktion einen Request ausführen.
        with ddragon_env(read_json={}, request_json={"v": "14.2.1"}) as m:
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
