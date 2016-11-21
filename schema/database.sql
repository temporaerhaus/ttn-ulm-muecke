CREATE TABLE `apps` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `userId` int(11) NOT NULL,
  `appEUI` varchar(255) NOT NULL,
  `appKey` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `data` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `appId` int(11) NOT NULL,
  `appEUI` varchar(255) NOT NULL,
  `payload` varchar(255) NOT NULL,
  `created` datetime DEFAULT CURRENT_TIMESTAMP,
  `raw` text,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=722 DEFAULT CHARSET=utf8;

CREATE TABLE `user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `email` varchar(255) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;