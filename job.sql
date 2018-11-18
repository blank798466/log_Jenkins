DROP TABLE IF EXISTS `logs`.`logs_pipeline`;

CREATE TABLE `logs`.`logs_pipeline` (
  `Pid` INT NOT NULL COMMENT '本次执行过程的id',
  `jobname` VARCHAR(45) NOT NULL COMMENT '本次job的name',
  `status` VARCHAR(45) NULL COMMENT '本次执行过程的状态，"FAILURE" or "SUCCESS"',
  `startTimeMillis` DATETIME NULL COMMENT '本次执行过程的开始时间，timestamp类型，转换公式为 time.localtime("startTimeMillis" / 1000 + 28800)',
  `endTimeMillis` DATETIME NULL COMMENT '本次执行过程的结束时间，timestamp类型',
  `durationMillis` VARCHAR(45) NULL COMMENT '本次执行过程消耗的时间，timestamp类型,转换公式为 durationMillis / 1000 s.',
  `queueDurationMillis` VARCHAR(45) NULL COMMENT '本次执行过程共有几个阶段，(最后对日志进行整理获取打包的脚本也属于一个阶段)',
  `pauseDurationMillis` VARCHAR(45) NULL COMMENT '本次执行过程中暂停中止的次数',
  `url` VARCHAR(45) NULL COMMENT '本次pipeline执行过程的描述地址',
  `changesets_url` VARCHAR(45) NULL COMMENT '本次执行过程的Changes信息描述地址',
  `stages_count` INT NULL COMMENT '本次执行过程中的stage阶段个数',
  PRIMARY KEY (`Pid`));