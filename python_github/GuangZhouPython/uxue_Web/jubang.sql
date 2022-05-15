/*
 Navicat Premium Data Transfer

 Source Server         : 本机mysql
 Source Server Type    : MySQL
 Source Server Version : 50725
 Source Host           : localhost:3306
 Source Schema         : jubang

 Target Server Type    : MySQL
 Target Server Version : 50725
 File Encoding         : 65001

 Date: 05/03/2019 23:43:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for add_mp_list
-- ----------------------------
DROP TABLE IF EXISTS `add_mp_list`;
CREATE TABLE `add_mp_list`  (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '要添加的公众号名称',
  `wx_hao` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '公众号的微信号',
  PRIMARY KEY (`_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for local_index_list
-- ----------------------------
DROP TABLE IF EXISTS `local_index_list`;
CREATE TABLE `local_index_list`  (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `ret_path` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '文章indexl地址',
  `coverName` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '封面图片地址',
  `artcleNum` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '本地文章编号',
  `wordT` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '本地文章正文',
  `zhuanyi` int(1) NULL DEFAULT NULL COMMENT '是否被转移0否1是',
  PRIMARY KEY (`_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 681 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for mp_info
-- ----------------------------
DROP TABLE IF EXISTS `mp_info`;
CREATE TABLE `mp_info`  (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '公众号名称',
  `wx_hao` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '公众号的微信号',
  `company` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '主体名称',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '功能简介',
  `logo_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT 'logo url',
  `qr_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '二维码URL',
  `create_time` datetime(0) NULL DEFAULT NULL COMMENT '加入牛榜时间',
  `update_time` datetime(0) NULL DEFAULT NULL COMMENT '最后更新时间',
  `rank_article_release_count` int(11) NULL DEFAULT 0 COMMENT '群发次数',
  `rank_article_count` int(11) NULL DEFAULT 0 COMMENT '群发篇数',
  `last_qunfa_id` int(30) NULL DEFAULT 0 COMMENT '最后的群发ID',
  `last_qufa_time` datetime(0) NULL DEFAULT NULL COMMENT '最后一次群发的时间',
  `wz_url` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '最近文章URL',
  PRIMARY KEY (`_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 291 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for webcontent
-- ----------------------------
DROP TABLE IF EXISTS `webcontent`;
CREATE TABLE `webcontent`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `artcleNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章唯一编号',
  `Content` mediumtext CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL,
  `numList` int(8) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 9047 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for weblist
-- ----------------------------
DROP TABLE IF EXISTS `weblist`;
CREATE TABLE `weblist`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `TitleT` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章标题',
  `artcleNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章唯一编号',
  `wx_hao` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '微信号',
  `categoriesChineseName` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '分类中文名称',
  `imgPath` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章所有图片本地地址',
  `dataTime` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章发布时间',
  `articlePreviewImg` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章预览图',
  `authorImg` varchar(1000) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '作者头像',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 210 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for webtags
-- ----------------------------
DROP TABLE IF EXISTS `webtags`;
CREATE TABLE `webtags`  (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `artcleNum` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '文章唯一编号',
  `tags0` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `tags0Vaule` int(10) NULL DEFAULT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 1903 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for wenzhang_info
-- ----------------------------
DROP TABLE IF EXISTS `wenzhang_info`;
CREATE TABLE `wenzhang_info`  (
  `_id` int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  `title` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '文章标题',
  `source_url` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '原文地址',
  `cover_url` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '封面图URL',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '文章摘要',
  `date_time` datetime(0) NULL DEFAULT NULL COMMENT '文章推送时间',
  `mp_id` int(11) NULL DEFAULT 0 COMMENT '对应的公众号ID',
  `read_count` int(11) NULL DEFAULT 0 COMMENT '阅读数',
  `like_count` int(11) NULL DEFAULT 0 COMMENT '点攒数',
  `comment_count` int(11) NULL DEFAULT 0 COMMENT '评论数',
  `content_url` varchar(300) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '文章永久地址',
  `author` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT '' COMMENT '作者',
  `msg_index` int(11) NULL DEFAULT 0 COMMENT '一次群发中的图文顺序 1是头条 ',
  `copyright_stat` int(1) NULL DEFAULT 0 COMMENT '11表示原创 其它表示非原创',
  `qunfa_id` int(30) NULL DEFAULT 0 COMMENT '群发消息ID',
  `type` int(11) NULL DEFAULT 0 COMMENT '消息类型',
  `artcleNum` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `zhuanyi` int(1) NULL DEFAULT NULL COMMENT '是否被转移0否1是',
  PRIMARY KEY (`_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7236 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
