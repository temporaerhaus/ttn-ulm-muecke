CREATE TABLE `apps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `app_id` varchar(120) NOT NULL,
  `app_key` varchar(120) NOT NULL,
  `settings` text,
  PRIMARY KEY (`id`),
  KEY `userid` (`userid`),
  CONSTRAINT `apps_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `dev_eui` varchar(120) DEFAULT NULL,
  `payload_raw` text,
  `payload_fields` text,
  `raw` text,
  `rssi` int(11) DEFAULT NULL,
  `snr` decimal(6,2) DEFAULT NULL,
  `gateway_eui` char(22) DEFAULT NULL,
  `received` varchar(150) DEFAULT NULL,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `data_app_id_created_index` (`app_id`,`created`),
  KEY `gateway_eui` (`gateway_eui`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=376518 DEFAULT CHARSET=utf8;

CREATE TABLE `data_gateway` (
  `id` int(11) NOT NULL,
  `gateway_eui` char(22) NOT NULL,
  `rssi` int(11) DEFAULT NULL,
  `snr` decimal(6,2) DEFAULT NULL,
  `received` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`,`gateway_eui`),
  KEY `gateway_eui` (`gateway_eui`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `password_reset` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_password_reset_token` (`token`),
  KEY `userid` (`userid`),
  CONSTRAINT `password_reset_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `registration_confirm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token` varchar(32) DEFAULT NULL,
  `userid` int(11) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_registration_confirm_token` (`token`),
  KEY `userid` (`userid`),
  CONSTRAINT `registration_confirm_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;