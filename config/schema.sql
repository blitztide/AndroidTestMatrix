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
  `Founded` int(11) DEFAULT NULL,
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

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`ApplicationID`) REFERENCES `Applications` (`ApplicationID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`Market`) REFERENCES `Marketplace` (`MarketID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`CertID`) REFERENCES `Certificate` (`CertID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Incident`) REFERENCES `Incident` (`IncidentID`);

ALTER TABLE `FailedRequests` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

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