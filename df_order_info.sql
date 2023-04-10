DROP TABLE IF EXISTS `df_order_info`;
CREATE TABLE `df_order_info` (
	  `create_time` datetime(6) NULL DEFAULT NULL,
	  `update_time` datetime(6) NULL DEFAULT NULL,
	  `is_delete` tinyint(1) NOT NULL,
	  `order_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	  `pay_method` smallint(0) NOT NULL,
	  `total_count` int(0) NOT NULL,
	  `total_price` decimal(10, 2) NOT NULL,
	  `transit_price` decimal(10, 2) NOT NULL,
	  `order_status` smallint(0) NOT NULL,
	  `trade_no` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	  `addr_id` int(0) NOT NULL,
	  `user_id` int(0) NOT NULL,
	  PRIMARY KEY (`order_id`) USING BTREE,
	  INDEX `df_order_info_addr_id_70c3726e_fk_df_address_id` (`addr_id`) USING BTREE,
	  INDEX `df_order_info_user_id_ac1e5bf5_fk_df_user_id` (`user_id`) USING BTREE,
	  CONSTRAINT `df_order_info_addr_id_70c3726e_fk_df_address_id` FOREIGN KEY (`addr_id`) REFERENCES `df_address` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
	  CONSTRAINT `df_order_info_user_id_ac1e5bf5_fk_df_user_id` FOREIGN KEY (`user_id`) REFERENCES `df_user` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci ROW_FORMAT=DYNAMIC;

