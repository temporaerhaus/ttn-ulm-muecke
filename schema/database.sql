CREATE TABLE `apps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` varchar(120) NOT NULL,
  `app_key` varchar(120) NOT NULL,
  `handler` VARCHAR(120) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

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
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`app_ id`) REFERENCES `apps` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `data_gateway` (
  `id` int(11) NOT NULL,
  `gateway_eui` char(22) NOT NULL,
  `rssi` int(11) DEFAULT NULL,
  `snr` decimal(6,2) DEFAULT NULL,
  `received` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`id`,`gateway_eui`),
  KEY `gateway_eui` (`gateway_eui`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



