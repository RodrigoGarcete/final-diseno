CREATE DATABASE  IF NOT EXISTS `sistema_pw2` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `sistema_pw2`;
-- MySQL dump 10.13  Distrib 8.0.26, for Win64 (x86_64)
--
-- Host: localhost    Database: sistema_pw2
-- ------------------------------------------------------
-- Server version	8.0.26

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categoria`
--

DROP TABLE IF EXISTS `categoria`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categoria` (
  `idcategoria` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `estado` tinyint DEFAULT NULL,
  PRIMARY KEY (`idcategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (2,'Desayunos','categoria desayunos','2022-11-18',1),(3,'prueba','probando','2022-11-18',0),(6,'Almuerzo','Categoria de almuerzo','2022-11-23',1),(11,'Bebidas','Categoria de bebidas','2022-11-23',1),(12,'snack','son snacks','2022-11-24',0),(13,'Acompanante','','2022-11-25',1),(15,'Dulce y salado','Cosas dulces y saladas en general','2022-12-06',1),(17,'Probando','Probando guardado de nueva categoria','2023-08-15',1);
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ciudad`
--

DROP TABLE IF EXISTS `ciudad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ciudad` (
  `idciudad` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `iddepartamento` int NOT NULL,
  PRIMARY KEY (`idciudad`),
  KEY `fk_ciudad_departamento1_idx` (`iddepartamento`),
  CONSTRAINT `fk_ciudad_departamento1` FOREIGN KEY (`iddepartamento`) REFERENCES `departamento` (`iddepartamento`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ciudad`
--

LOCK TABLES `ciudad` WRITE;
/*!40000 ALTER TABLE `ciudad` DISABLE KEYS */;
INSERT INTO `ciudad` VALUES (1,'Coronel Oviedo',1),(2,'Caaguazu',1),(3,'San Joaquin',1),(4,'Villarrica',2);
/*!40000 ALTER TABLE `ciudad` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cliente`
--

DROP TABLE IF EXISTS `cliente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cliente` (
  `idcliente` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `ruc` varchar(45) DEFAULT NULL,
  `idciudad` int NOT NULL,
  `telefono` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idcliente`),
  KEY `idciudad_idx` (`idciudad`),
  CONSTRAINT `idciudad` FOREIGN KEY (`idciudad`) REFERENCES `ciudad` (`idciudad`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Sin Nombre',NULL,NULL,1,NULL),(2,'Rodrigo','Portillo','5679938',1,'0976415999'),(3,'Nathalia','Gonzalez','1234567',4,'099872734'),(4,'Karen','Gonzalez','5745298',3,'09887176');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `departamento`
--

DROP TABLE IF EXISTS `departamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `departamento` (
  `iddepartamento` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `idpais` int NOT NULL,
  PRIMARY KEY (`iddepartamento`),
  KEY `fk_departamento_pais1_idx` (`idpais`),
  CONSTRAINT `fk_departamento_pais1` FOREIGN KEY (`idpais`) REFERENCES `pais` (`idpais`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `departamento`
--

LOCK TABLES `departamento` WRITE;
/*!40000 ALTER TABLE `departamento` DISABLE KEYS */;
INSERT INTO `departamento` VALUES (1,'Caaguazu',0),(2,'Guaira',0);
/*!40000 ALTER TABLE `departamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_facturacion`
--

DROP TABLE IF EXISTS `detalle_facturacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_facturacion` (
  `idmenu` int NOT NULL,
  `idfacturacion` int NOT NULL,
  `precio` int DEFAULT NULL,
  `cantidad` int DEFAULT NULL,
  PRIMARY KEY (`idmenu`,`idfacturacion`),
  KEY `fk_menu_has_facturacion_facturacion1_idx` (`idfacturacion`),
  KEY `fk_menu_has_facturacion_menu1_idx` (`idmenu`),
  CONSTRAINT `fk_menu_has_facturacion_facturacion1` FOREIGN KEY (`idfacturacion`) REFERENCES `facturacion` (`idfacturacion`),
  CONSTRAINT `fk_menu_has_facturacion_menu1` FOREIGN KEY (`idmenu`) REFERENCES `menu` (`idmenu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_facturacion`
--

LOCK TABLES `detalle_facturacion` WRITE;
/*!40000 ALTER TABLE `detalle_facturacion` DISABLE KEYS */;
INSERT INTO `detalle_facturacion` VALUES (1,122,5000,1),(11,121,12000,1);
/*!40000 ALTER TABLE `detalle_facturacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facturacion`
--

DROP TABLE IF EXISTS `facturacion`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facturacion` (
  `idfacturacion` int NOT NULL AUTO_INCREMENT,
  `total` int DEFAULT NULL,
  `idcliente` int NOT NULL,
  `idusuario` int NOT NULL,
  `orden` int DEFAULT NULL,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `estado` int DEFAULT NULL,
  PRIMARY KEY (`idfacturacion`,`idcliente`,`idusuario`),
  KEY `fk_facturacion_cliente1_idx` (`idcliente`),
  KEY `fk_facturacion_usuario1_idx` (`idusuario`),
  CONSTRAINT `fk_facturacion_cliente1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`),
  CONSTRAINT `fk_facturacion_usuario1` FOREIGN KEY (`idusuario`) REFERENCES `usuario` (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=123 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facturacion`
--

LOCK TABLES `facturacion` WRITE;
/*!40000 ALTER TABLE `facturacion` DISABLE KEYS */;
INSERT INTO `facturacion` VALUES (121,12000,4,4,1,'2023-08-24','09:55:44',1),(122,5000,4,4,2,'2023-08-24','09:56:15',0);
/*!40000 ALTER TABLE `facturacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `menu`
--

DROP TABLE IF EXISTS `menu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `menu` (
  `idmenu` int NOT NULL AUTO_INCREMENT,
  `fecha_creacion` date DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `precio` int DEFAULT NULL,
  `estado` varchar(45) DEFAULT NULL,
  `imagen` varchar(100) DEFAULT NULL,
  `idcategoria` int NOT NULL,
  PRIMARY KEY (`idmenu`),
  KEY `fk_menu_categoria_idx` (`idcategoria`),
  CONSTRAINT `fk_menu_categoria` FOREIGN KEY (`idcategoria`) REFERENCES `categoria` (`idcategoria`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'2022-11-24','papas fritas','Las papas fritas o patatas fritas, también conocidas como papas a la belga, patatas a la belga o papas francesas o chips, son las papas que se preparan cortándose en forma de bastones y friéndolas en ',5000,'1','Papas-Fritas.jpg',6),(6,'2022-11-25','Hamburguesas','Doble Carne con Chedar',11000,'1','img-menu-2.jpeg',2),(7,'2022-11-26','Lomito Arabe','Lomito árabe mixto (carne y pollo) ',15000,'1','img-menu-7.jpg',2),(10,'2022-11-28','Pizza','La pizza es una preparación culinaria que consiste en un pan plano, habitualmente de forma circular, elaborado con harina de trigo, levadura, agua y sal',40000,'1','img-menu-10.jpg',6),(11,'2022-12-06','Milkshake','Es una bebida elaborada a base de leche o helado, que puede llevar frutas, chocolate o turrón, por ejemplo. Los batidos de frutas pueden ser hechos de diferentes maneras. ',12000,'1','img-menu-11.jpg',11),(12,'2022-12-06','Examen','examen',10000,'0','',6);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pais`
--

DROP TABLE IF EXISTS `pais`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pais` (
  `idpais` int NOT NULL,
  `nombre` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idpais`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pais`
--

LOCK TABLES `pais` WRITE;
/*!40000 ALTER TABLE `pais` DISABLE KEYS */;
/*!40000 ALTER TABLE `pais` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reserva`
--

DROP TABLE IF EXISTS `reserva`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reserva` (
  `idreserva` int NOT NULL AUTO_INCREMENT,
  `fecha` date DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `num_mesa` int DEFAULT NULL,
  `num_personas` int DEFAULT NULL,
  `nota` text,
  `estado` int DEFAULT NULL,
  `idcliente` int NOT NULL,
  `cedula` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`idreserva`),
  KEY `fk_reserva_cliente1_idx` (`idcliente`),
  CONSTRAINT `fk_reserva_cliente1` FOREIGN KEY (`idcliente`) REFERENCES `cliente` (`idcliente`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reserva`
--

LOCK TABLES `reserva` WRITE;
/*!40000 ALTER TABLE `reserva` DISABLE KEYS */;
INSERT INTO `reserva` VALUES (4,'2023-08-24','03:38:00',2,4,'',0,2,'5679938'),(5,'2023-08-24','05:46:00',2,2,'reservado para un festejo de despedida',0,1,'32523'),(6,'2023-08-24','22:09:00',2,2,'',1,1,'1525765'),(7,'2023-08-25','22:13:00',3,2,'',1,2,'5679938'),(8,'2023-08-26','22:16:00',1,1,'',1,1,'1525765'),(9,'2023-08-24','05:16:00',1,1,'',1,1,'1525765');
/*!40000 ALTER TABLE `reserva` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuario`
--

DROP TABLE IF EXISTS `usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuario` (
  `idusuario` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(50) DEFAULT NULL,
  `apellido` varchar(50) DEFAULT NULL,
  `usuario` varchar(45) DEFAULT NULL,
  `pass` varchar(200) DEFAULT NULL,
  `rol` int DEFAULT NULL,
  `fecha_creacion` date DEFAULT NULL,
  `estado` tinyint DEFAULT NULL,
  PRIMARY KEY (`idusuario`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (3,'Rodrigo','Garcete','rodri','$2y$05$.tR.ATNl1TDtLblosWimwuUaHM0.Wij5Vt6P7mRupqfd3dr0SbSWi',1,'2022-11-27',1),(4,'administrador','administrador','admin','$2b$12$IGoo7Z9ZnZUvDRnJ3qyfGOGdkAZeBZCoBkC5/OV3IQEco4.qFLQE2',2,'2022-11-27',1),(5,'pepito','','cocinero','$2b$12$JkO9QaMK14HBgoMsbLs.Y.f9Dr4D0/eZqIqGrh0wBW0RuG6rqgWgK',3,'2022-12-05',1);
/*!40000 ALTER TABLE `usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-08-24 20:37:51
