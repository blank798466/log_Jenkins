DROP TABLE IF EXISTS `logs_stages`;

CREATE TABLE `logs`.`logs_stages` (
  `Sid` CHAR(4) NOT NULL,
  `Pid` CHAR(4) NOT NULL,
  `Sname` VARCHAR(45) NOT NULL,
  `SexecNode` VARCHAR(45) NOT NULL,
  `Sstatus` VARCHAR(45) NULL,
  `SerrorMessage` VARCHAR(45) NULL,
  `SerrorType` VARCHAR(45) NULL,
  `SstartTimeMillis` DATETIME NULL,
  `SdurationMillis` VARCHAR(45) NULL,
  `SpauseDurationMillis` VARCHAR(45) NULL,
  `Surl` VARCHAR(45) NULL,
  `Cnodes_count` INT DEFAULT 0,
  PRIMARY KEY (`Sid`));