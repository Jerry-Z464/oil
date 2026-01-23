/*
 Navicat Premium Data Transfer

 Source Server         : mysql_localhost
 Source Server Type    : MySQL
 Source Server Version : 80027
 Source Host           : localhost:3306
 Source Schema         : oil_well

 Target Server Type    : MySQL
 Target Server Version : 80027
 File Encoding         : 65001

 Date: 23/01/2026 14:47:19
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '名称',
  `password` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '密码',
  `email` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '邮箱',
  `profile_photo` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NULL DEFAULT NULL COMMENT '头像',
  `phone_number` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL COMMENT '手机号码',
  `dept_id` bigint NULL DEFAULT NULL COMMENT '部门id',
  `role` tinyint NOT NULL COMMENT '角色',
  `work` tinyint NOT NULL DEFAULT 1 COMMENT '是否在职 1是 0否',
  `remark` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '用户备注',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 4 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alarm
-- ----------------------------
DROP TABLE IF EXISTS `alarm`;
CREATE TABLE `alarm`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `code` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '设备编码',
  `alarm_type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '告警类型',
  `level` tinyint NULL DEFAULT NULL COMMENT '告警级别',
  `metric` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '指标标识',
  `current_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '当前指标值',
  `threshold` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '阈值',
  `suggestion` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '处理建议',
  `alarm_time` datetime NULL DEFAULT NULL COMMENT '告警触发时间',
  `status` tinyint NULL DEFAULT NULL COMMENT '通知状态',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for alert
-- ----------------------------
DROP TABLE IF EXISTS `alert`;
CREATE TABLE `alert`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID（自增）',
  `device_id` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '设备ID',
  `alert_level` tinyint NULL DEFAULT NULL COMMENT '告警级别',
  `metric` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '指标标识',
  `current_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '当前指标值',
  `threshold` varchar(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '阈值',
  `suggestion` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '处理建议',
  `trigger_time` datetime NULL DEFAULT NULL COMMENT '告警触发时间',
  `notification_status` tinyint NULL DEFAULT NULL COMMENT '通知状态',
  `notification_channels` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知渠道',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '告警信息表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for audit_logs
-- ----------------------------
DROP TABLE IF EXISTS `audit_logs`;
CREATE TABLE `audit_logs`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `log_type` tinyint NULL DEFAULT NULL COMMENT '日志类型',
  `log_content` varchar(500) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '日志内容',
  `log_time` datetime NULL DEFAULT NULL COMMENT '日志时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '审计日志表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for correction_record
-- ----------------------------
DROP TABLE IF EXISTS `correction_record`;
CREATE TABLE `correction_record`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `data_time` datetime NULL DEFAULT NULL COMMENT '数据时间',
  `modify_time` datetime NULL DEFAULT NULL COMMENT '修改时间',
  `correction_type` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '修正类型',
  `field` varchar(30) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字段名称',
  `original_data` decimal(10, 2) NULL DEFAULT NULL COMMENT '原始数据（百分比类数据存数值，如12.50对应12.50%）',
  `modified_data` decimal(10, 2) NULL DEFAULT NULL COMMENT '修改后数据',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '修正记录表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for data_fields
-- ----------------------------
DROP TABLE IF EXISTS `data_fields`;
CREATE TABLE `data_fields`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `field_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字段名称',
  `description` varchar(200) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字段描述',
  `data_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '数据类型',
  `default_value` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '默认值',
  `unit` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '字段单位',
  `storage_format` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '存储格式',
  `status` bigint NULL DEFAULT NULL COMMENT '状态标识',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '数据字段配置表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for dept
-- ----------------------------
DROP TABLE IF EXISTS `dept`;
CREATE TABLE `dept`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '自增id，部门id',
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '部门名称',
  `parent_id` bigint NOT NULL COMMENT '父级id',
  `full_parent_id` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL DEFAULT '' COMMENT '全路径id',
  `level` tinyint NOT NULL DEFAULT 0 COMMENT '等级',
  `principal` bigint NULL DEFAULT NULL COMMENT '部门负责人id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for deviation_comparison
-- ----------------------------
DROP TABLE IF EXISTS `deviation_comparison`;
CREATE TABLE `deviation_comparison`  (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键ID（自增）',
  `time` datetime NULL DEFAULT NULL COMMENT '数据记录时间',
  `differential_pressure` decimal(10, 2) NULL DEFAULT NULL COMMENT '差压',
  `gas_volume_fraction` decimal(10, 2) NULL DEFAULT NULL COMMENT '气体体积分数',
  `gas_flow_rate` decimal(10, 2) NULL DEFAULT NULL COMMENT '气体流速',
  `liquid_flow_rate` decimal(10, 2) NULL DEFAULT NULL COMMENT '液体流速',
  `oil_flow_rate` decimal(10, 2) NULL DEFAULT NULL COMMENT '油流速',
  `pressure` decimal(10, 2) NULL DEFAULT NULL COMMENT '压力',
  `temperature` decimal(10, 2) NULL DEFAULT NULL COMMENT '温度',
  `water_cut` decimal(10, 2) NULL DEFAULT NULL COMMENT '含水率',
  `water_flow_rate` decimal(10, 2) NULL DEFAULT NULL COMMENT '水流速',
  `status` int NULL DEFAULT NULL COMMENT '状态标识',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '偏差对比数据表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for deviation_comparison_results
-- ----------------------------
DROP TABLE IF EXISTS `deviation_comparison_results`;
CREATE TABLE `deviation_comparison_results`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `current_deviation` decimal(5, 2) NULL DEFAULT NULL COMMENT '当前偏差值',
  `high_deviation_point` int NULL DEFAULT NULL COMMENT '高偏差点',
  `correction_applied` enum('Yes','No') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '是否应用修正',
  `stat_time` datetime NULL DEFAULT NULL COMMENT '统计时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '偏差对比结果表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for device
-- ----------------------------
DROP TABLE IF EXISTS `device`;
CREATE TABLE `device`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for employees
-- ----------------------------
DROP TABLE IF EXISTS `employees`;
CREATE TABLE `employees`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '员工ID（主键）',
  `employee_name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '员工姓名',
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '手机号码',
  `email` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '电子邮箱',
  `employment_status` enum('Employed','Resigned') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT ' employment状态（在职/离职）',
  `position` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '职位',
  `role` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '角色',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '员工信息表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for formula_correction
-- ----------------------------
DROP TABLE IF EXISTS `formula_correction`;
CREATE TABLE `formula_correction`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `dp` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'dp字段（示例值：2+6）',
  `gVF` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'gVF字段（示例值：56*5）',
  `waterCut` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'waterCut字段（示例值：56/74）',
  `pressure` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT 'pressure字段',
  `updated_time` datetime NULL DEFAULT NULL COMMENT '更新时间',
  `Status` bigint NULL DEFAULT NULL COMMENT '状态标识',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '公式修正表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for notification_settings
-- ----------------------------
DROP TABLE IF EXISTS `notification_settings`;
CREATE TABLE `notification_settings`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `notification_methods` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '通知方式',
  `alert_suppression_tin` int NULL DEFAULT NULL COMMENT '告警抑制标识',
  `recipients` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '接收者信息',
  `created_at` datetime NULL DEFAULT NULL COMMENT '创建时间',
  `updated_at` datetime NULL DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 2 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '通知配置表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for type_dict
-- ----------------------------
DROP TABLE IF EXISTS `type_dict`;
CREATE TABLE `type_dict`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型编码',
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '基础类型名称',
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '描述',
  `label` tinyint NOT NULL DEFAULT 0 COMMENT '0系统配置 1自定义配置',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for type_dict_content
-- ----------------------------
DROP TABLE IF EXISTS `type_dict_content`;
CREATE TABLE `type_dict_content`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '类型编码',
  `type_id` bigint NOT NULL COMMENT '类型字典id',
  `content` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '类型内容名称',
  `rank` tinyint NOT NULL DEFAULT 1 COMMENT '排序',
  `parent` bigint NOT NULL DEFAULT 0 COMMENT '上级类型id',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user
-- ----------------------------
DROP TABLE IF EXISTS `user`;
CREATE TABLE `user`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `username` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '微信昵称',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '微信头像url',
  `role` tinyint NOT NULL DEFAULT 1 COMMENT '角色',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for user_token
-- ----------------------------
DROP TABLE IF EXISTS `user_token`;
CREATE TABLE `user_token`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `user_id` bigint NOT NULL,
  `token` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `timestamp` bigint NOT NULL,
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 3 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for water_cut_sample
-- ----------------------------
DROP TABLE IF EXISTS `water_cut_sample`;
CREATE TABLE `water_cut_sample`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `sample` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '样本点',
  `start_sampling_time` datetime NOT NULL COMMENT '开始采样时间',
  `end_sampling_time` datetime NOT NULL COMMENT '结束采样时间',
  `rolling_avg` decimal(10, 2) NULL DEFAULT NULL COMMENT '滚动平均值',
  `deviation_threshold` decimal(10, 2) NULL DEFAULT NULL COMMENT '偏差阈值',
  `deviation_avg` decimal(10, 2) NULL DEFAULT NULL COMMENT '偏差平均值',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '含水率数据表' ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for well_data
-- ----------------------------
DROP TABLE IF EXISTS `well_data`;
CREATE TABLE `well_data`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '自增id，用户id',
  `code` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `dp` decimal(10, 2) NOT NULL,
  `gvf` decimal(10, 2) NOT NULL,
  `gas_flow_rate` decimal(10, 2) NOT NULL,
  `liquid_flow_rate` decimal(10, 2) NOT NULL,
  `oil_flow_rate` decimal(10, 2) NOT NULL,
  `pressure` decimal(10, 2) NOT NULL,
  `temperature` decimal(10, 2) NOT NULL,
  `water_cut` decimal(10, 2) NOT NULL,
  `water_flow_rate` decimal(10, 2) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `valid` tinyint NOT NULL DEFAULT 1 COMMENT '是否有效 1是 0否',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
