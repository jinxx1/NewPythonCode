/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80013
 Source Host           : localhost:3306
 Source Schema         : uxsq_analyse

 Target Server Type    : MySQL
 Target Server Version : 80013
 File Encoding         : 65001

 Date: 18/08/2019 21:59:20
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for bugfileinfo
-- ----------------------------
DROP TABLE IF EXISTS `bugfileinfo`;
CREATE TABLE `bugfileinfo`  (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `bugFile` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '  读取错误的excel',
  `reLoad` int(5) UNSIGNED ZEROFILL NOT NULL COMMENT ' 是否已经重新读取0否1是',
  `BugExplain` varchar(3000) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '备注说明',
  `reLoadsueccful` int(1) UNSIGNED ZEROFILL NOT NULL COMMENT ' 是否已经重新读取0否1是',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 276 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
