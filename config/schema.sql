CREATE DATABASE hack;
USE hack;

DROP TABLE IF EXISTS `Applications`;

CREATE TABLE `Applications` (
  `ApplicationID` int(11) NOT NULL AUTO_INCREMENT,
  `PackageName` text DEFAULT NULL,
  `Version` text DEFAULT NULL,
  `IsMalware` bit(1) DEFAULT NULL,
  `MD5Sum` text DEFAULT NULL,
  `SHA1Sum` text DEFAULT NULL,
  `SHA256Sum` text DEFAULT NULL,
  `AppDate` datetime DEFAULT NULL,
  `AddedDate` datetime DEFAULT NULL,
  PRIMARY KEY (`ApplicationID`),
  KEY `hash` (`SHA256Sum`(1024))
) ENGINE=InnoDB AUTO_INCREMENT=20033206 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `Availability`;

CREATE TABLE `Availability` (
  `AvailabilityID` int(11) NOT NULL AUTO_INCREMENT,
  `ApplicationID` int(11) DEFAULT NULL,
  `MarketID` int(11) DEFAULT NULL,
  PRIMARY KEY (`AvailabilityID`)
);

DROP TABLE IF EXISTS `Certificate`;
CREATE TABLE `Certificate` (
  `CertID` int(11) NOT NULL AUTO_INCREMENT,
  `CertificateType` text DEFAULT NULL,
  `fingerprint` text DEFAULT NULL,
  `FullCertificate` longblob DEFAULT NULL,
  PRIMARY KEY (`CertID`),
  UNIQUE KEY `fingerprint_u` (`fingerprint`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Certificates`;
CREATE TABLE `Certificates` (
  `CertificatesID` int(11) NOT NULL AUTO_INCREMENT,
  `CertID` int(11) DEFAULT NULL,
  `Domain` int(11) DEFAULT NULL,
  PRIMARY KEY (`CertificatesID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Companies`;

CREATE TABLE `Companies` (
  `CompanyID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` text DEFAULT NULL,
  `Exists` int(11) DEFAULT NULL,
  `Founded` datetime DEFAULT NULL,
  PRIMARY KEY (`CompanyID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS `Domains`;

CREATE TABLE `Domains` (
  `DomainID` int(11) NOT NULL AUTO_INCREMENT,
  `URI` text DEFAULT NULL,
  `domain_age` int(11) DEFAULT NULL,
  `KnownC2` int(11) DEFAULT NULL,
  `HasSSL` bit(1) DEFAULT NULL,
  `SSLVersion` int(11) DEFAULT NULL,
  `IP` text DEFAULT NULL,
  `Country` text DEFAULT NULL,
  `AvailableApps` int(11) DEFAULT NULL,
  PRIMARY KEY (`DomainID`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `FailedRequests`;

CREATE TABLE `FailedRequests` (
  `RequestID` int(11) NOT NULL AUTO_INCREMENT,
  `Domain` int(11) DEFAULT NULL,
  `StartTime` datetime DEFAULT NULL,
  `EndTime` datetime DEFAULT NULL,
  PRIMARY KEY (`RequestID`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Incident`;

CREATE TABLE `Incident` (
  `IncidentID` int(11) NOT NULL AUTO_INCREMENT,
  `IncidentDate` datetime DEFAULT NULL,
  `Info` text DEFAULT NULL,
  PRIMARY KEY (`IncidentID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Incidents`;

CREATE TABLE `Incidents` (
  `IncidentsID` int(11) NOT NULL AUTO_INCREMENT,
  `Company` int(11) DEFAULT NULL,
  `Incident` int(11) DEFAULT NULL,
  PRIMARY KEY (`IncidentsID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

DROP TABLE IF EXISTS `Marketplace`;

CREATE TABLE `Marketplace` (
  `MarketID` int(11) NOT NULL AUTO_INCREMENT,
  `name` text DEFAULT NULL,
  `Company` int(11) DEFAULT NULL,
  `Domain` int(11) DEFAULT NULL,
  `DomainScore` int(11) DEFAULT NULL,
  `MarketScore` int(11) DEFAULT NULL,
  `CompanyScore` int(11) DEFAULT NULL,
  PRIMARY KEY (`MarketID`),
  UNIQUE KEY `name` (`name`) USING HASH
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=latin1;


INSERT INTO Domains (URI) VALUES ("https://play.google.com");
INSERT INTO Domains (URI) VALUES ("https://www.amazon.com/mobile-apps");
INSERT INTO Domains (URI) VALUES ("https://apkmirror.com");
INSERT INTO Domains (URI) VALUES ("https://www.f-droid.org");
INSERT INTO Domains (URI) VALUES ("https://galaxystore.samsung.com");
INSERT INTO Domains (URI) VALUES ("https://apkpure.com");
INSERT INTO Domains (URI) VALUES ("https://aptoide.com");
INSERT INTO Domains (URI) VALUES ("http://slideme.org");
INSERT INTO Domains (URI) VALUES ("https://www.getjar.com");
INSERT INTO Domains (URI) VALUES ("https://en.uptodown.com/android");
INSERT INTO Domains (URI) VALUES ("https://www.appbrain.com");
INSERT INTO Domains (URI) VALUES ("https://auroraoss.com");
INSERT INTO Domains (URI) VALUES ("https://appgallery.huawei.com");
INSERT INTO Domains (URI) VALUES ("https://1mobile.market");
INSERT INTO Domains (URI) VALUES ("http://www.mobango.com");
INSERT INTO Domains (URI) VALUES ("https://www.mobile9.com");

INSERT into Marketplace ( name ) VALUES ( "google play");
INSERT into Marketplace ( name ) VALUES ( "amazon app store");
INSERT into Marketplace ( name ) VALUES ( "apkmirror");
INSERT into Marketplace ( name ) VALUES ( "fdroid");
INSERT into Marketplace ( name ) VALUES ( "samsung galaxy app store");
INSERT into Marketplace ( name ) VALUES ( "apkpure");
INSERT into Marketplace ( name ) VALUES ( "aptoide");
INSERT into Marketplace ( name ) VALUES ( "slideme");
INSERT into Marketplace ( name ) VALUES ( "getjar");
INSERT into Marketplace ( name ) VALUES ( "uptodown");
INSERT into Marketplace ( name ) VALUES ( "appbrain");
INSERT into Marketplace ( name ) VALUES ( "aurora store");
INSERT into Marketplace ( name ) VALUES ( "huawei app gallery");
INSERT into Marketplace ( name ) VALUES ( "1mobile");
INSERT into Marketplace ( name ) VALUES ( "mobango");
INSERT into Marketplace ( name ) VALUES ( "mobile9");

UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://www.amazon.com/mobile-apps") WHERE name = 'amazon app store';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://play.google.com") WHERE name = 'google play';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://apkmirror.com") WHERE name = 'apkmirror';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://www.f-droid.org") WHERE name = 'fdroid';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://galaxystore.samsung.com") WHERE name = 'samsung galaxy app store';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://apkpure.com") WHERE name = 'apkpure';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://aptoide.com") WHERE name = 'aptoide';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "http://slideme.org") WHERE name = 'slideme';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://www.getjar.com") WHERE name = 'getjar';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://en.uptodown.com/android") WHERE name = 'uptodown';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://www.appbrain.com") WHERE name = 'appbrain';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://auroraoss.com") WHERE name = 'aurora store';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://appgallery.huawei.com") WHERE name = 'huawei app gallery';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://1mobile.market") WHERE name = '1mobile';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "http://www.mobango.com") WHERE name = 'mobango';
UPDATE Marketplace SET Domain = ( SELECT DomainID FROM Domains WHERE URI = "https://www.mobile9.com") WHERE name = 'mobile9';

INSERT into Companies VALUES (1, 'NOCOMPANY', 0 , NULL);
INSERT into Companies VALUES (2, "Google Inc.", 1, "1998-09-04 00:00:00");
INSERT into Companies VALUES (3, "Amazon", 1, "1994-07-05 00:00:00");
INSERT into Companies VALUES (4, "ILLOGICAL ROBOT LLC", 1, "2012-04-23 00:00:00");
INSERT into Companies VALUES (5, "F-DROID LIMITED", 1, "2013-02-26 00:00:00");
INSERT into Companies VALUES (6, "Samsung", 1, "1938-03-01 00:00:00");
INSERT into Companies VALUES (7, "APKPure", 1, "2014-01-01 00:00:00");
INSERT into Companies VALUES (8, "Aptoide S.A.", 1, "2011-08-01 00:00:00");
INSERT into Companies VALUES (9, "SlideME", 1, "2008-01-01 00:00:00");
INSERT into Companies VALUES (10, "GetJar Baltic UAB.", 1, "2004-01-01 00:00:00");
INSERT into Companies VALUES (11, "Uptodown ", 1, "2002-01-01 00:00:00");
INSERT into Companies VALUES (12, "AppTornado GmbH", 1, "2009-11-01 00:00:00");
INSERT into Companies VALUES (13, "Huawei", 1, "1987-09-15 00:00:00");
INSERT into Companies VALUES (14, "Mobango", 0, "2006-01-01 00:00:00");
INSERT into Companies VALUES (15, "Mobile9", 1, "2003-10-10 00:00:00");

UPDATE Marketplace SET Company = 2 WHERE name = 'google play';
UPDATE Marketplace SET Company = 3 WHERE name = 'amazon app store';
UPDATE Marketplace SET Company = 4 WHERE name = 'apkmirror';
UPDATE Marketplace SET Company = 5 WHERE name = 'fdroid';
UPDATE Marketplace SET Company = 6 WHERE name = 'samsung galaxy app store';
UPDATE Marketplace SET Company = 7 WHERE name = 'apkpure';
UPDATE Marketplace SET Company = 8 WHERE name = 'aptoide';
UPDATE Marketplace SET Company = 9 WHERE name = 'slideme';
UPDATE Marketplace SET Company = 10 WHERE name = 'getjar';
UPDATE Marketplace SET Company = 11 WHERE name = 'uptodown';
UPDATE Marketplace SET Company = 12 WHERE name = 'appbrain';
UPDATE Marketplace SET Company = 1 WHERE name = 'aurora store';
UPDATE Marketplace SET Company = 13 WHERE name = 'huawei app gallery';
UPDATE Marketplace SET Company = 1 WHERE name = '1mobile';
UPDATE Marketplace SET Company = 14 WHERE name = 'mobango';
UPDATE Marketplace SET Company = 15 WHERE name = 'mobile9';

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`ApplicationID`) REFERENCES `Applications` (`ApplicationID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`MarketID`) REFERENCES `Marketplace` (`MarketID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`CertID`) REFERENCES `Certificate` (`CertID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Incident`) REFERENCES `Incident` (`IncidentID`);

ALTER TABLE `FailedRequests` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);