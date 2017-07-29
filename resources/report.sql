CREATE TABLE `moodle_db`.`mdl_workshop_plag` (
  `plag_id` BIGINT(10) NOT NULL AUTO_INCREMENT,
  `author_id` BIGINT(10) NOT NULL,
  `sentence_id` INT(5) NOT NULL,
  `sentence_content` LONGTEXT NULL,
  `ref1_content` LONGTEXT NULL,
  `ref1_similarity` DECIMAL(10,5) NULL,
  `ref2_content` LONGTEXT NULL,
  `ref2_similarity` DECIMAL(10,5) NULL,
  PRIMARY KEY (`plag_id`));

  CREATE TABLE `moodle_db`.`mdl_workshop_plag_report` (
  `item_id` BIGINT(10) NOT NULL AUTO_INCREMENT,
  `author_id` BIGINT(10) NOT NULL,
  `author_name` VARCHAR(45) NOT NULL,
  `title` VARCHAR(200) NOT NULL,
  `sentence_cnt` INT(5) NOT NULL,
  `plg_cnt` INT(5) NOT NULL,
  `plg_cent` DECIMAL(10,5) NOT NULL,
  `ws_grading` DECIMAL(10,5) NOT NULL,
  PRIMARY KEY (`item_id`));