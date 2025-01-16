-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3307
-- Generation Time: Jan 16, 2025 at 05:47 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `beberas`
--

-- --------------------------------------------------------

--
-- Table structure for table `batal_keluar`
--

CREATE TABLE `batal_keluar` (
  `id_keluar` varchar(255) NOT NULL,
  `tanggal_batal` date NOT NULL,
  `keterangan` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `batal_keluar`
--

INSERT INTO `batal_keluar` (`id_keluar`, `tanggal_batal`, `keterangan`) VALUES
('K2025011602', '2025-01-16', 'bismillah'),
('K2025011603', '2025-01-16', 'tidak valid');

-- --------------------------------------------------------

--
-- Table structure for table `stok`
--

CREATE TABLE `stok` (
  `barang` varchar(255) NOT NULL,
  `jumlah` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `stok`
--

INSERT INTO `stok` (`barang`, `jumlah`) VALUES
('10kg', 5),
('25kg', 5),
('5kg', 20);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_keluar`
--

CREATE TABLE `transaksi_keluar` (
  `id_keluar` varchar(255) NOT NULL,
  `tanggal_keluar` date DEFAULT NULL,
  `barang_keluar` varchar(255) DEFAULT NULL,
  `jumlah_keluar` int(11) DEFAULT NULL,
  `harga_total_keluar` float DEFAULT NULL,
  `total_harga_kulak` float DEFAULT NULL,
  `keuntungan` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi_keluar`
--

INSERT INTO `transaksi_keluar` (`id_keluar`, `tanggal_keluar`, `barang_keluar`, `jumlah_keluar`, `harga_total_keluar`, `total_harga_kulak`, `keuntungan`) VALUES
('K2025011501', '2025-01-15', '5kg', 13, 883000, 818000, 65000),
('K2025011502', '2025-01-15', '5kg', 5, 340000, 318500, 21500),
('K2025011503', '2025-01-15', '10kg', 5, 670000, 645000, 25000),
('K2025011504', '2025-01-15', '25kg', 1, 335000, 330000, 5000),
('K2025011506', '2025-01-15', '10kg', 2, 272000, 262000, 10000),
('K2025011507', '2025-01-15', '25kg', 6, 2000000, 1970000, 30000),
('K2025011601', '2025-01-16', '5kg', 0, 0, 0, 0),
('K2025011602', '2025-01-16', '5kg', 0, 0, 0, 0),
('K2025011603', '2025-01-16', '5kg', 0, 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `transaksi_masuk`
--

CREATE TABLE `transaksi_masuk` (
  `id_masuk` varchar(255) NOT NULL,
  `tanggal_masuk` date DEFAULT NULL,
  `barang_masuk` varchar(255) DEFAULT NULL,
  `jumlah_masuk` int(11) DEFAULT NULL,
  `harga_total_masuk` float DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `transaksi_masuk`
--

INSERT INTO `transaksi_masuk` (`id_masuk`, `tanggal_masuk`, `barang_masuk`, `jumlah_masuk`, `harga_total_masuk`) VALUES
('K2025011601', '2025-01-16', '10kg', 5, 645000),
('M2025010901', '2025-01-09', '5kg', 10, 627500),
('M2025010902', '2025-01-09', '5kg', 2, 128000),
('M2025011101', '2025-01-11', '25kg', 5, 1640000),
('M2025011401', '2025-01-14', '10kg', 10, 1287500),
('M2025011501', '2025-01-15', '5kg', 13, 818000),
('M2025011502', '2025-01-15', '5kg', 13, 818000);

-- --------------------------------------------------------

--
-- Table structure for table `user`
--

CREATE TABLE `user` (
  `username` varchar(50) NOT NULL,
  `password` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user`
--

INSERT INTO `user` (`username`, `password`) VALUES
('naswa', 'pboa'),
('raisa', 'raisa123');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `stok`
--
ALTER TABLE `stok`
  ADD PRIMARY KEY (`barang`);

--
-- Indexes for table `transaksi_keluar`
--
ALTER TABLE `transaksi_keluar`
  ADD PRIMARY KEY (`id_keluar`);

--
-- Indexes for table `transaksi_masuk`
--
ALTER TABLE `transaksi_masuk`
  ADD PRIMARY KEY (`id_masuk`);

--
-- Indexes for table `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`username`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
