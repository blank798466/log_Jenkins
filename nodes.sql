DROP TABLE IF EXISTS `logs_nodes`;

CREATE TABLE `logs`.`logs_nodes` (
  `Nid` CHAR(4) NOT NULL,
  `Sid` CHAR(4) NOT NULL,
  `Nname` VARCHAR(45) NOT NULL,
  `NexecNode` VARCHAR(45) NOT NULL,
  `Nstatus` VARCHAR(45) NULL,
  `NerrorMessage` VARCHAR(45) NULL,
  `NerrorType` VARCHAR(45) NULL,
  `NerrorParameterDescription` VARCHAR(45) NULL,
  `NstartTimeMillis` DATETIME NULL,
  `NdurationMillis` VARCHAR(45) NULL,
  `NpauseDurationMillis` VARCHAR(45) NULL,
  `Nurl` VARCHAR(45) NULL,
  `NlogUrl` VARCHAR(45) NULL,
  `NtextLength` VARCHAR(45) NULL,
  `NtextContent` VARCHAR(200) NULL,
  PRIMARY KEY (`Nid`));