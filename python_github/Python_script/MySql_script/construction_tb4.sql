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

 Date: 30/08/2019 04:18:36
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for construction_tb4
-- ----------------------------
DROP TABLE IF EXISTS `construction_tb4`;
CREATE TABLE `construction_tb4`  (
  `id` int(20) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `excel_id` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'excel序列号',
  `certificate_Name` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '证书名称',
  `certificate_Num` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '证书编号',
  `certificate_Institution` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '认证/审核发放机构',
  `certificate_Range` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '认证范围/资质等级',
  `certificate_GetTime` datetime(0) NULL DEFAULT NULL COMMENT '颁发日期',
  `certificate_Indate` datetime(0) NULL DEFAULT NULL COMMENT '有效期至',
  `from_excel_path` varchar(3000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT 'excel文件路径',
  `perfectItem` int(1) UNSIGNED NULL DEFAULT NULL COMMENT '所在表内的行数',
  `Name` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '申报厂商名称',
  `sheetName` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '是否为移动业务',
  `excel_rownum` int(30) NULL DEFAULT NULL COMMENT '所在表内的行数',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 52812 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
