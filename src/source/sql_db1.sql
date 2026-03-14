/*
SQLyog Trial v13.2.1 (64 bit)
MySQL - 8.0.37 : Database - nl_to_sql_db
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`nl_to_sql_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `nl_to_sql_db`;

/*Table structure for table `class_info` */

DROP TABLE IF EXISTS `class_info`;

CREATE TABLE `class_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '班级ID',
  `class_name` varchar(32) NOT NULL COMMENT '班级名称',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='班级信息表';

/*Data for the table `class_info` */

insert  into `class_info`(`id`,`class_name`) values 
(1,'一班'),
(2,'二班'),
(3,'三班');

/*Table structure for table `class_teacher_map` */

DROP TABLE IF EXISTS `class_teacher_map`;

CREATE TABLE `class_teacher_map` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `class_id` bigint NOT NULL COMMENT '班级ID',
  `teacher_id` bigint NOT NULL COMMENT '教师ID',
  `subject_id` bigint DEFAULT NULL COMMENT '所教科目ID',
  PRIMARY KEY (`id`),
  KEY `fk_class_teacher_class` (`class_id`),
  KEY `fk_class_teacher_teacher` (`teacher_id`),
  KEY `fk_class_teacher_subject` (`subject_id`),
  CONSTRAINT `fk_class_teacher_class` FOREIGN KEY (`class_id`) REFERENCES `class_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_class_teacher_subject` FOREIGN KEY (`subject_id`) REFERENCES `subject_info` (`id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_class_teacher_teacher` FOREIGN KEY (`teacher_id`) REFERENCES `teacher_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='班级_教师_所教科目映射表';

/*Data for the table `class_teacher_map` */

insert  into `class_teacher_map`(`id`,`class_id`,`teacher_id`,`subject_id`) values 
(2,1,1,1),
(3,1,2,2),
(4,1,3,3),
(6,2,4,1),
(7,2,4,2),
(8,2,5,3),
(9,3,6,1),
(10,3,2,2),
(11,3,5,3);

/*Table structure for table `student_info` */

DROP TABLE IF EXISTS `student_info`;

CREATE TABLE `student_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '学号',
  `stu_name` varchar(32) DEFAULT NULL COMMENT '姓名',
  `age` int DEFAULT NULL COMMENT '年龄',
  `sex` int DEFAULT NULL COMMENT '性别：1=男；2=女',
  `stu_class` bigint DEFAULT NULL COMMENT '班级ID',
  PRIMARY KEY (`id`),
  KEY `fk_student_class` (`stu_class`),
  CONSTRAINT `fk_student_class` FOREIGN KEY (`stu_class`) REFERENCES `class_info` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生信息表';

/*Data for the table `student_info` */

insert  into `student_info`(`id`,`stu_name`,`age`,`sex`,`stu_class`) values 
(1,'张三',11,1,NULL),
(2,'李四',12,2,NULL),
(3,'王五',12,1,NULL),
(4,'洪六',13,2,NULL),
(5,'钱七',14,1,NULL);

/*Table structure for table `student_score` */

DROP TABLE IF EXISTS `student_score`;

CREATE TABLE `student_score` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `stu_id` bigint NOT NULL COMMENT '学号',
  `subject_id` bigint DEFAULT NULL COMMENT '科目ID',
  `score` decimal(4,1) DEFAULT NULL COMMENT '分数',
  `exam_type` varchar(64) DEFAULT NULL COMMENT '考试类型',
  PRIMARY KEY (`id`),
  KEY `fk_score_student` (`stu_id`),
  KEY `fk_score_subject` (`subject_id`),
  CONSTRAINT `fk_score_student` FOREIGN KEY (`stu_id`) REFERENCES `student_info` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_score_subject` FOREIGN KEY (`subject_id`) REFERENCES `subject_info` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='学生成绩表';

/*Data for the table `student_score` */

insert  into `student_score`(`id`,`stu_id`,`subject_id`,`score`,`exam_type`) values 
(1,1,1,80.0,'期末考试'),
(2,1,2,95.0,'期末考试'),
(3,1,3,95.5,'期末考试'),
(4,2,1,69.0,'期末考试'),
(5,2,2,85.0,'期末考试'),
(6,2,3,75.0,'期末考试'),
(7,3,1,52.0,'期末考试'),
(8,3,2,74.0,'期末考试'),
(9,3,3,99.0,'期末考试'),
(10,4,1,100.0,'期末考试'),
(11,4,2,96.0,'期末考试'),
(12,4,3,48.0,'期末考试'),
(13,5,1,0.0,'期末考试'),
(14,5,2,66.0,'期末考试'),
(15,5,3,87.0,'期末考试');

/*Table structure for table `subject_info` */

DROP TABLE IF EXISTS `subject_info`;

CREATE TABLE `subject_info` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(32) NOT NULL COMMENT '科目名称，比如：语文、数学、英语、物理等学科',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='科目信息表';

/*Data for the table `subject_info` */

insert  into `subject_info`(`id`,`subject_name`) values 
(1,'英语'),
(2,'语文'),
(3,'数学');

/*Table structure for table `teacher_info` */

DROP TABLE IF EXISTS `teacher_info`;

CREATE TABLE `teacher_info` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '教师ID',
  `teacher_name` varchar(32) NOT NULL COMMENT '教师姓名',
  `tel` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL COMMENT '电话号码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='教师信息表';

/*Data for the table `teacher_info` */

insert  into `teacher_info`(`id`,`teacher_name`,`tel`) values 
(1,'陆小凤','13854125652'),
(2,'花满楼','13854125651'),
(3,'西门吹雪','13854125653'),
(4,'谢晓峰','13854125654'),
(5,'韩立','13854125655'),
(6,'张小凡','13854125656'),
(7,'向之礼','13854125657');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;