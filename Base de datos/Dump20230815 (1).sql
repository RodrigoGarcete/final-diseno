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
-- Dumping data for table `categoria`
--

LOCK TABLES `categoria` WRITE;
/*!40000 ALTER TABLE `categoria` DISABLE KEYS */;
INSERT INTO `categoria` VALUES (2,'Desayunos','categoria desayunos','2022-11-18',1),(3,'prueba','probando','2022-11-18',0),(6,'Almuerzo','Categoria de almuerzo','2022-11-23',1),(11,'Bebidas','Categoria de bebidas','2022-11-23',1),(12,'snack','son snacks','2022-11-24',0),(13,'Acompanante','','2022-11-25',1),(15,'Dulce y salado','Cosas dulces y saladas en general','2022-12-06',1),(17,'Probando','Probando guardado de nueva categoria','2023-08-15',1);
/*!40000 ALTER TABLE `categoria` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `cliente`
--

LOCK TABLES `cliente` WRITE;
/*!40000 ALTER TABLE `cliente` DISABLE KEYS */;
INSERT INTO `cliente` VALUES (1,'Sin Nombre',NULL,NULL),(2,'Rodrigo','Garcete','5679938');
/*!40000 ALTER TABLE `cliente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `detalle_facturacion`
--

LOCK TABLES `detalle_facturacion` WRITE;
/*!40000 ALTER TABLE `detalle_facturacion` DISABLE KEYS */;
INSERT INTO `detalle_facturacion` VALUES (1,4,5000,1),(1,7,5000,1),(1,8,5000,1),(1,9,5000,1),(1,10,5000,2),(1,11,5000,2),(1,12,5000,2),(1,13,5000,2),(1,14,5000,2),(1,15,5000,2),(1,16,5000,2),(1,17,5000,2),(1,18,5000,2),(1,19,5000,2),(1,20,5000,2),(1,21,5000,3),(1,22,5000,3),(1,23,5000,3),(1,24,5000,1),(1,32,5000,3),(1,36,5000,1),(1,39,5000,1),(1,41,5000,1),(1,49,5000,1),(1,53,5000,1),(6,4,11000,2),(6,7,11000,4),(6,10,11000,2),(6,11,11000,2),(6,12,11000,2),(6,13,11000,2),(6,14,11000,2),(6,15,11000,2),(6,16,11000,2),(6,17,11000,2),(6,18,11000,2),(6,19,11000,2),(6,20,11000,2),(6,24,11000,1),(6,33,11000,1),(6,39,11000,1),(6,44,11000,1),(6,47,11000,1),(6,48,11000,1),(6,50,11000,1),(6,53,11000,1),(7,4,15000,2),(7,8,15000,1),(7,9,15000,1),(7,11,15000,3),(7,12,15000,3),(7,13,15000,3),(7,14,15000,3),(7,15,15000,3),(7,16,15000,3),(7,17,15000,3),(7,18,15000,3),(7,19,15000,3),(7,20,15000,3),(7,21,15000,3),(7,22,15000,3),(7,23,15000,3),(7,24,15000,1),(7,31,15000,1),(7,40,15000,1),(7,42,15000,1),(7,43,15000,1),(7,52,15000,2),(7,53,15000,1),(7,54,15000,2),(10,4,40000,1),(10,8,40000,1),(10,9,40000,1),(10,11,40000,1),(10,12,40000,1),(10,13,40000,1),(10,14,40000,1),(10,15,40000,1),(10,16,40000,1),(10,17,40000,1),(10,18,40000,1),(10,19,40000,1),(10,20,40000,1),(10,21,40000,2),(10,22,40000,2),(10,23,40000,2),(10,24,40000,1),(10,25,40000,3),(10,34,40000,1),(10,35,40000,2),(10,37,40000,1),(10,38,40000,1),(10,39,40000,1),(10,45,40000,1),(10,46,40000,4),(10,53,40000,1),(11,51,12000,1),(11,54,12000,1),(12,52,10000,1);
/*!40000 ALTER TABLE `detalle_facturacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `facturacion`
--

LOCK TABLES `facturacion` WRITE;
/*!40000 ALTER TABLE `facturacion` DISABLE KEYS */;
INSERT INTO `facturacion` VALUES (4,97000,1,3,NULL,'2022-12-03','15:11:52',1),(7,49000,1,3,1,'2022-12-03','17:41:25',1),(8,60000,1,3,2,'2022-12-03','18:36:49',1),(9,60000,1,3,3,'2022-12-03','18:37:54',1),(10,32000,1,3,4,'2022-12-03','18:39:22',1),(11,117000,1,3,5,'2022-12-03','18:52:08',1),(12,117000,1,3,6,'2022-12-03','18:53:55',1),(13,117000,1,3,7,'2022-12-03','18:54:38',1),(14,117000,1,3,8,'2022-12-03','18:57:08',1),(15,117000,1,3,9,'2022-12-03','19:12:41',1),(16,117000,1,3,10,'2022-12-03','19:13:12',1),(17,117000,1,3,11,'2022-12-03','19:13:44',1),(18,117000,1,3,12,'2022-12-03','19:16:25',1),(19,117000,1,3,13,'2022-12-03','19:17:23',1),(20,117000,1,3,14,'2022-12-03','19:19:29',1),(21,140000,1,3,15,'2022-12-03','19:25:44',1),(22,140000,1,3,16,'2022-12-03','19:31:04',1),(23,140000,1,3,17,'2022-12-03','19:56:35',1),(24,71000,1,3,18,'2022-12-03','19:56:54',1),(25,120000,1,3,1,'2022-12-04','10:17:00',1),(26,3000000,1,3,1,'2022-11-05','10:18:00',1),(27,1000000,1,3,1,'2022-10-10','10:10:00',1),(28,2000000,1,3,1,'2022-09-01','12:00:00',1),(29,500000,1,3,1,'2022-08-01','09:00:00',1),(30,600000,1,3,1,'2022-07-02','12:00:00',1),(31,15000,1,3,1,'2022-12-05','21:13:22',1),(32,15000,1,3,2,'2022-12-05','21:22:32',1),(33,11000,1,3,3,'2022-12-05','21:27:29',1),(34,40000,1,3,4,'2022-12-05','21:31:04',1),(35,80000,1,3,5,'2022-12-05','21:33:04',1),(36,5000,1,3,6,'2022-12-05','21:37:45',1),(37,40000,1,3,7,'2022-12-05','21:46:42',1),(38,40000,1,3,8,'2022-12-05','21:48:35',1),(39,56000,1,3,9,'2022-12-05','21:59:19',1),(40,15000,1,3,10,'2022-12-05','22:00:36',1),(41,5000,1,3,1,'2022-12-06','09:16:20',1),(42,15000,1,3,2,'2022-12-06','09:17:10',0),(43,15000,1,3,3,'2022-12-06','09:27:20',0),(44,11000,2,3,4,'2022-12-06','09:27:49',0),(45,40000,1,3,5,'2022-12-06','09:36:52',1),(46,160000,1,3,6,'2022-12-06','15:11:06',0),(47,11000,2,3,7,'2022-12-06','15:14:05',0),(48,11000,1,3,8,'2022-12-06','15:15:00',0),(49,5000,1,3,9,'2022-12-06','15:16:05',0),(50,11000,1,3,10,'2022-12-06','15:21:42',0),(51,12000,1,3,11,'2022-12-06','16:07:45',0),(52,40000,2,3,12,'2022-12-06','18:27:26',0),(53,71000,1,3,13,'2022-12-06','18:28:48',1),(54,42000,1,3,1,'2023-08-07','15:12:27',1);
/*!40000 ALTER TABLE `facturacion` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `menu`
--

LOCK TABLES `menu` WRITE;
/*!40000 ALTER TABLE `menu` DISABLE KEYS */;
INSERT INTO `menu` VALUES (1,'2022-11-24','papas fritas','Las papas fritas o patatas fritas, también conocidas como papas a la belga, patatas a la belga o papas francesas o chips, son las papas que se preparan cortándose en forma de bastones y friéndolas en ',5000,'1','Papas-Fritas.jpg',6),(6,'2022-11-25','Hamburguesas','Doble Carne con Chedar',11000,'1','img-menu-2.jpeg',2),(7,'2022-11-26','Lomito Arabe','Lomito árabe mixto (carne y pollo) ',15000,'1','img-menu-7.jpg',2),(10,'2022-11-28','Pizza','La pizza es una preparación culinaria que consiste en un pan plano, habitualmente de forma circular, elaborado con harina de trigo, levadura, agua y sal',40000,'1','img-menu-10.jpg',6),(11,'2022-12-06','Milkshake','Es una bebida elaborada a base de leche o helado, que puede llevar frutas, chocolate o turrón, por ejemplo. Los batidos de frutas pueden ser hechos de diferentes maneras. ',12000,'1','img-menu-11.jpg',11),(12,'2022-12-06','Examen','examen',10000,'1','',6);
/*!40000 ALTER TABLE `menu` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping data for table `usuario`
--

LOCK TABLES `usuario` WRITE;
/*!40000 ALTER TABLE `usuario` DISABLE KEYS */;
INSERT INTO `usuario` VALUES (3,'Rodrigo','Garcete','rodri','$2y$05$.tR.ATNl1TDtLblosWimwuUaHM0.Wij5Vt6P7mRupqfd3dr0SbSWi',1,'2022-11-27',1),(4,'administrador','administrador','admin','$2y$05$IIuiK4BP8EZP6QRCll5uPeAeUu.1h8MdInyfeaYI40BctOY7RNttS',1,'2022-11-27',1),(5,'pepito','','cocinero','$2y$05$efvDPZZ70JgOAq9Aso8yYuM58kYScBVcSpWF5YuKjULBzTigu7Pc2',3,'2022-12-05',1);
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

-- Dump completed on 2023-08-15 15:54:13
