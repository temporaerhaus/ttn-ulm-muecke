CREATE TABLE `apps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userid` int(11) DEFAULT NULL,
  `app_id` varchar(120) NOT NULL,
  `app_key` varchar(120) NOT NULL,
  `settings` text,
  PRIMARY KEY (`id`),
  KEY `userid` (`userid`),
  CONSTRAINT `apps_ibfk_1` FOREIGN KEY (`userid`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_id` int(11) DEFAULT NULL,
  `dev_eui` varchar(120) DEFAULT NULL,
  `payload_raw` text,
  `payload_fields` text,
  `raw` text,
  `rssi` int(11) DEFAULT NULL,
  `snr` int(11) DEFAULT NULL,
  `gateway_eui` text,
  `received` text,
  `created` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `app_id` (`app_id`),
  CONSTRAINT `data_ibfk_1` FOREIGN KEY (`app_id`) REFERENCES `apps` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2803 DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;