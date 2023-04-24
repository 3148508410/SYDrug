DROP TABLE IF EXISTS `df_order_goods`;
CREATE TABLE `df_order_goods`  (
	  `id` int(0) NOT NULL AUTO_INCREMENT,
	  `create_time` datetime(6) NULL DEFAULT NULL,
	  `update_time` datetime(6) NULL DEFAULT NULL,
	  `is_delete` tinyint(1) NOT NULL,
	  `count` int(0) NOT NULL,
	  `price` decimal(10, 2) NOT NULL,
	  `comment` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	  `order_id` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
	  `sku_id` int(0) NOT NULL,
	  PRIMARY KEY (`id`) USING BTREE,
	  INDEX `df_order_goods_order_id_6958ee23_fk_df_order_info_order_id`(`order_id`) USING BTREE,
	  INDEX `df_order_goods_sku_id_b7d6e04e_fk_df_goods_sku_id`(`sku_id`) USING BTREE,
	  CONSTRAINT `df_order_goods_order_id_6958ee23_fk_df_order_info_order_id` FOREIGN KEY (`order_id`) REFERENCES `df_order_info` (`order_id`) ON DELETE RESTRICT ON UPDATE RESTRICT,
	  CONSTRAINT `df_order_goods_sku_id_b7d6e04e_fk_df_goods_sku_id` FOREIGN KEY (`sku_id`) REFERENCES `df_goods_sku` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 56 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
