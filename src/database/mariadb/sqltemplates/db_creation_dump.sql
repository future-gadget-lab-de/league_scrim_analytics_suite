SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";

CREATE TABLE `metadata` (
  `gameid` bigint(20) NOT NULL,
  `patch` text NOT NULL,
  `date` date NOT NULL,
  `duration` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
--
-- Table structure for table `playerdata`
--

CREATE TABLE `playerdata` (
  `gameid` bigint(20) NOT NULL,
  `playerid` varchar(16) NOT NULL,
  `teamid` int(11) NOT NULL,
  `champ` text NOT NULL,
  `summ1` text NOT NULL,
  `summ2` text NOT NULL,
  `item1` text NOT NULL,
  `item2` text NOT NULL,
  `item3` text NOT NULL,
  `item4` text NOT NULL,
  `item5` text NOT NULL,
  `item6` text NOT NULL,
  `item7` text NOT NULL,
  `rune1` text NOT NULL,
  `rune2` text NOT NULL,
  `rune3` text NOT NULL,
  `rune4` text NOT NULL,
  `rune5` text NOT NULL,
  `rune6` text NOT NULL,
  `cwards_bought` int(11) NOT NULL,
  `wards_placed` int(11) NOT NULL,
  `wards_destroyed` int(11) NOT NULL,
  `vision_score` int(11) NOT NULL,
  `minions_killed` int(11) NOT NULL,
  `own_jng_kill` int(11) NOT NULL,
  `ene_jng_kill` int(11) NOT NULL,
  `kills` int(11) NOT NULL,
  `deaths` int(11) NOT NULL,
  `assists` int(11) NOT NULL,
  `damage_dealt` int(11) NOT NULL,
  `gold_earned` int(11) NOT NULL,
  `turret_dmg` int(11) NOT NULL,
  `team` varchar(16) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------
--
-- Table structure for table `teamdata`
--

CREATE TABLE `teamdata` (
  `gameid` bigint(20) NOT NULL,
  `teamid` int(11) NOT NULL,
  `ban1` text NOT NULL,
  `ban2` text NOT NULL,
  `ban3` text NOT NULL,
  `ban4` text NOT NULL,
  `ban5` text NOT NULL,
  `barons` int(11) NOT NULL,
  `dragons` int(11) NOT NULL,
  `herald` int(11) NOT NULL,
  `grubs` int(11) NOT NULL,
  `firstbl` tinyint(1) NOT NULL,
  `firstto` tinyint(1) NOT NULL,
  `firstdr` tinyint(1) NOT NULL,
  `firstbr` tinyint(1) NOT NULL,
  `win` tinyint(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
--
-- Indexes for table `metadata`
--
ALTER TABLE `metadata`
  ADD PRIMARY KEY (`gameid`);
--
-- Indexes for table `playerdata`
--
ALTER TABLE `playerdata`
  ADD PRIMARY KEY (`gameid`,`playerid`);
--
-- Indexes for table `teamdata`
--
ALTER TABLE `teamdata`
  ADD PRIMARY KEY (`gameid`,`teamid`);
COMMIT;
