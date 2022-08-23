CREATE DATABASE test;
USE test;
CREATE TABLE `Domains` (
  `DomainID` int PRIMARY KEY,
  `name` TEXT,
  `URI` TEXT,
  `domain_age` int,
  `KnownC2` int,
  `HasSSL` bit,
  `SSLVersion` int,
  `IP` TEXT,
  `Country` TEXT,
  `AvailableApps` int
);

CREATE TABLE `Applications` (
  `ApplicationID` int PRIMARY KEY,
  `PackageName` TEXT,
  `Version` TEXT,
  `Architecture` TEXT,
  `IsMalware` bit,
  `MD5Sum` TEXT,
  `SHA1Sum` TEXT,
  `SHA256Sum` TEXT,
  `AppDate` datetime,
  `AddedDate` datetime
);

CREATE TABLE `Certificate` (
  `CertID` int PRIMARY KEY,
  `CertificateType` TEXT,
  `fingerprint` TEXT unique,
  `FullCertificate` longblob
);

CREATE TABLE `Marketplace` (
  `MarketID` int PRIMARY KEY,
  `name` TEXT,
  `Company` int,
  `Domain` int,
  `DomainScore` int,
  `MarketScore` int,
  `CompanyScore` int
);

CREATE TABLE `Companies` (
  `CompanyID` int PRIMARY KEY,
  `Exists` int,
  `Founded` int
);

CREATE TABLE `Availability` (
  `AvailabilityID` int PRIMARY KEY,
  `ApplicationID` int,
  `Market` int
);

CREATE TABLE `Certificates` (
  `CertificatesID` int PRIMARY KEY,
  `CertID` int,
  `Domain` int
);

CREATE TABLE `Incident` (
  `IncidentID` int PRIMARY KEY,
  `IncidentDate` datetime,
  `Info` TEXT
);

CREATE TABLE `Incidents` (
  `IncidentsID` int PRIMARY KEY,
  `Company` int,
  `Incident` int
);

CREATE TABLE `FailedRequests` (
  `RequestID` int PRIMARY KEY,
  `Domain` int,
  `StartTime` datetime,
  `EndTime` datetime
);

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Marketplace` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`ApplicationID`) REFERENCES `Applications` (`ApplicationID`);

ALTER TABLE `Availability` ADD FOREIGN KEY (`Market`) REFERENCES `Marketplace` (`MarketID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`CertID`) REFERENCES `Certificate` (`CertID`);

ALTER TABLE `Certificates` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Company`) REFERENCES `Companies` (`CompanyID`);

ALTER TABLE `Incidents` ADD FOREIGN KEY (`Incident`) REFERENCES `Incident` (`IncidentID`);

ALTER TABLE `FailedRequests` ADD FOREIGN KEY (`Domain`) REFERENCES `Domains` (`DomainID`);
