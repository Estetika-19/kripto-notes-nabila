-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 10, 2025 at 11:31 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `notes_app`
--

-- --------------------------------------------------------

--
-- Table structure for table `notes`
--

CREATE TABLE `notes` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `content_encrypted` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notes`
--

INSERT INTO `notes` (`id`, `user_id`, `title`, `content_encrypted`) VALUES
(1, 3, 'This is testing diary', '}X@UGGTVVETZ_YBV@^GVA^VU\\YAEGXVAAXZPUY^^@XEC[TXQVPWFVBX\\PRXxVGRRGB\\TVPG_@VYVX@ZPQ@TFRY_FPP@_]T[wRZ@BPDCGG^GWXX[]G^YVAF\\E]T[GT@DC^XQ\\BsVEQV\\EEAXGTY^uV\\_BAT@UP]]TF_D]C\\P\\TTAXTAT@AEVBP\\@PB]_EUBGV\\@TWW@TZUZ]FRQFETWBAGTSGFDGZQ@BPUTXZ]QBA][[[FYAWSGRBG_UQ_wWU_[]@US_@EPDFAV[[^GWSBBWX[_W[S[B@YN_G@DFWZSWCAGZ[]C[YW\Zr\\W[AUXAF^]W[S]BA]\ZDZXFG_AqUUGWQFAEWSB[WZAWQZEBUS@DGQY]GWFFUBABAQbUE\\YAEWXB\\XWAP\\VE^SZ[WWqFTFFWQ_Qv]W__ZZSSWZWQCAU[S\\XGCFQFXQ^YGDB@F@@B@AX]XA]bUS^GF@@B@Q_XB]WXWQFSQCQSS]U@W@T^YE_QV[@^QSTZZZC>CQ_SCSBADS[CB@Z]QBU[[FQ_]]QQQ_PB^AS]BAB@@UGDX[G]BZ[ZCQ[XFDEWQ[UUB[@GWAvZUQZC\\DFUXAU]ZDrEW@[]YGFS]XQZSG@PG]CdWWXEAYSQ_@RQA@BRu_GYU\\A[]CQ\ZD@SFZ_G@SUC[_YBQWSW][[FGDA]CR_[Av]FFEAR_UXW[WWWABQ[\\A^@AXX_BT_AAXVEGU]F]@ZDXZP@P|WSG^TFXGzVD]A]CVPZD[]BAPZU\\ATAGD@V@TT[ETB[@X[_DAATVVE\\FZ@@]TFXEEZF_Q]tRED][AR_\\T\\R]TR^\\PR@FF^\\E\\ETY\\CDE_FVg\\FTGZTYVCV9BCVXPR_YRPP}BTE]P[ZTFTX\\AbP@RT@XA@TZAP@DA\\RCT_TRPABPCFRPWB@VCYFXXRPYR^P]BXZV]IV@EP`W\\W\\^XDVRGFT\\_Y@]XRGGT'),
(2, 3, 'This is another testing', '}X@UGGTVVETZ_YBV@^GVA^VU\\YAEGXVAAXZPUY^^@XEC[TXQVPWFVBX\\PRXxVGRRGB\\TVPG_@VYVX@ZPQ@TFRY_FPP@_]T[wRZ@BPDCGG^GWXX[]G^YVAF\\E]T[GT@DC^XQ\\BsVEQV\\EEAXGTY^uV\\_BAT@UP]]TF_D]C\\P\\TTAXTAT@AEVBP\\@PB]_EUBGV\\@TWW@TZUZ]FRQFETWBAGTSGFDGZQ@BPUTXZ]QBA][[[FYAWSGRBG_UQ_wWU_[]@US_@EPDFAV[[^GWSBBWX[_W[S[B@YN_G@DFWZSWCAGZ[]C[YW\Zr\\W[AUXAF^]W[S]BA]\ZDZXFG_AqUUGWQFAEWSB[WZAWQZEBUS@DGQY]GWFFUBABAQbUE\\YAEWXB\\XWAP\\VE^SZ[WWqFTFFWQ_Qv]W__ZZSSWZWQCAU[S\\XGCFQFXQ^YGDB@F@@B@AX]XA]bUS^GF@@B@Q_XB]WXWQFSQCQSS]U@W@T^YE_QV[@^QSTZZZC>CQ_SCSBADS[CB@Z]QBU[[FQ_]]QQQ_PB^AS]BAB@@UGDX[G]BZ[ZCQ[XFDEWQ[UUB[@GWAvZUQZC\\DFUXAU]ZDrEW@[]YGFS]XQZSG@PG]CdWWXEAYSQ_@RQA@BRu_GYU\\A[]CQ\ZD@SFZ_G@SUC[_YBQWSW][[FGDA]CR_[Av]FFEAR_UXW[WWWABQ[\\A^@AXX_BT_AAXVEGU]F]@ZDXZP@P|WSG^TFXGzVD]A]CVPZD[]BAPZU\\ATAGD@V@TT[ETB[@X[_DAATVVE\\FZ@@]TFXEEZF_Q]tRED][AR_\\T\\R]TR^\\PR@FF^\\E\\ETY\\CDE_FVg\\FTGZTYVCV9BCVXPR_YRPP}BTE]P[ZTFTX\\AbP@RT@XA@TZAP@DA\\RCT_TRPABPCFRPWB@VCYFXXRPYR^P]BXZV]IV@EP`W\\W\\^XDVRGFT\\_Y@]XRGGT'),
(3, 3, 'Ini testing lain', '}X@UGGTVVETZ_Y]QBA][[[FYAWSGRBG_UQ_AXX_BT_AAXVE'),
(4, 3, 'Another another test', '}X@UGGTVVETZ_YBV@^GVA^VU\\YAEGXVAAXZPUY^^@XEC[TXQVPWFVBX\\PRXxVGRRGB\\TVPG_@VYVX@ZPQ@TFRY_FPP@_]T[wRZ@BPDCGG^GWXX[]G^YVAF\\E]T[GT@DC^XQ\\BsVEQV\\EEAXGTY^uV\\_BAT@UP]]TF_D]C\\P\\TTAXTAT@AEVBP\\@PB]_EUBGV\\@TWW@TZUZ]FRQFETWBAGTSGFDGZQ@BPUTXZ]QBA][[[FYAWSGRBG_UQ_wWU_[]@US_@EPDFAV[[^GWSBBWX[_W[S[B@YN_G@DFWZSWCAGZ[]C[YW\Zr\\W[AUXAF^]W[S]BA]\ZDZXFG_AqUUGWQFAEWSB[WZAWQZEBUS@DGQY]GWFFUBABAQbUE\\YAEWXB\\XWAP\\VE^SZ[WWqFTFFWQ_Qv]W__ZZSSWZWQCAU[S\\XGCFQFXQ^YGDB@F@@B@AX]XA]bUS^GF@@B@Q_XB]WXWQFSQCQSS]U@W@T^YE_QV[@^QSTZZZC>CQ_SCSBADS[CB@Z]QBU[[FQ_]]QQQ_PB^AS]BAB@@UGDX[G]BZ[ZCQ[XFDEWQ[UUB[@GWAvZUQZC\\DFUXAU]ZDrEW@[]YGFS]XQZSG@PG]CdWWXEAYSQ_@RQA@BRu_GYU\\A[]CQ\ZD@SFZ_G@SUC[_YBQWSW][[FGDA]CR_[Av]FFEAR_UXW[WWWABQ[\\A^@AXX_BT_AAXVEGU]F]@ZDXZP@P|WSG^TFXGzVD]A]CVPZD[]BAPZU\\ATAGD@V@TT[ETB[@X[_DAATVVE\\FZ@@]TFXEEZF_Q]tRED][AR_\\T\\R]TR^\\PR@FF^\\E\\ETY\\CDE_FVg\\FTGZTYVCV9BCVXPR_YRPP}BTE]P[ZTFTX\\AbP@RT@XA@TZAP@DA\\RCT_TRPABPCFRPWB@VCYFXXRPYR^P]BXZV]IV@EP`W\\W\\^XDVRGFT\\_Y@]XRGGT'),
(5, 3, 'Ini test laiin', 'XEAPX_TEE_PE_PEEZXBPUX'),
(6, 3, 'Ini test laiin dengan titikl', 'xPPX_AZXE_PEEZXPUX'),
(7, 3, 'Lagi', '~_AV@FWQWFS[\\^AQA]@W@]WV[^@F@[WF@[]QV^_]A[D@\\U[VWSVAWA__WS[W@SQ@A[WQWF\\GW^W[G[SVASGQ^^AQSG\\\\W\\vQ]AAWGDFF]@V[_Z^F]^WFG_B\\W\\FWAGB][V]A]WBG]][_F]AQWGVBA[UW[qSS[[[@SW_FAV@FGV]_^ASSDFW\\[[W]W]F@_J_ADD@S\\WWGAA^[[G[]Wv\\Q_AS\\AB^[S]S[FA[D\\\\FA[GqSUASWBACSUF[Q^ASQ\\ABSW@@GW][GQBFSFGFAWbSA\\]ACS^F\\^SGT\\PA^U^]SWq@PF@SW[Wv[W[_\\^SWW\\SWGGQ]WZ\\GGFUF^U^]GBFFB@FF@G\\[\\A[bSW^AB@FF@W[^F[S^SQ@WWGWWS[UFWFP^_A_WV]D^WWT\\Z\\G@[_^AS\\F@[QF@T^A\\G[G_[SGS{VPF]SG[@{UC^F\\@WS[G\\\\AFW[V[@WFFGGWGWSZFSA\\A[\\^GF@WQWF[G[GA^SG[DF]G\\V^sSFC\\\\@QX]W[S^SS][SUAAG][F[DW^]@CD\\AWd[GW@[W^W@Q'),
(8, 3, '1 lagi pakai 2 paragraf', '~_AV@FWQWFS[\\^AQA]@W@]WV[^@F@[WF@[]QV^_]A[D@\\U[VWSVAWA__WS[W@SQ@A[WQWF\\GW^W[G[SVASGQ^^AQSG\\\\W\\vQ]AAWGDFF]@V[_Z^F]^WFG_B\\W\\FWAGB][V]A~_AV@FWQWFS[\\^AQA]@W@]WV[^@F@[WF@[]QV^_]A[D@\\U[VWSVAWA__WS[W@SQ@A[WQWF\\GW^W[G[SVASGQ^^AQSG\\\\W\\vQ]AAWGDFF]@V[_Z^F]^WFG_B\\W\\FWAGB][V]A]WBG]][_F]AQWGVBA[UW[qSS[[[@SW_FAV@FGV]_^ASSDFW\\[[W]W]F@_J_ADD@S\\WWGAA^[[G[]Wv\\Q_AS\\AB^[S]S[FA[D\\\\FA[GqSUASWBACSUF[Q^ASQ\\ABSW@@GW][GQBFSFGFAWbSA\\]ACS^F\\^SGT\\PA^U^]SWq@PF@SW[Wv[W[_\\^SWW\\SWGGQ]WZ\\GGFUF^U^]GBFFB@FF@G\\[\\A[bSW^AB@FF@W[^F[S^SQ@WWGWWS[UFWFP^_A_WV]D^WWT\\Z\\G8]WBG]][_F]AQWGVBA[UW[qSS[[[@SW_FAV@FGV]_^ASSDFW\\[[W]W]F@_J_ADD@S\\WWGAA^[[G[]Wv\\Q_AS\\AB^[S]S[FA[D\\\\FA[GqSUASWBACSUF[Q^ASQ\\ABSW@@GW][GQBFSFGFAWbSA\\]ACS^F\\^SGT\\PA^U^]SWq@PF@SW[Wv[W[_\\^SWW\\SWGGQ]WZ\\GGFUF^U^]GBFFB@FF@G\\[\\A[bSW^AB@FF@W[^F[S^SQ@WWGWWS[UFWFP^_A_WV]D^WWT\\Z\\G@[_^AS\\F@[QF@T^A\\G[G_[SGS{VPF]SG[@{UC^F\\@WS[G\\\\AFW[V[@WFFGGWGWSZFSA\\A[\\^GF@WQWF[G[GA^SG[DF]G\\V^sSFC\\\\@QX]W[S^SS][SUAAG][F[DW^]@CD\\AWd[GW@[W^W@Q8@[_^AS\\F@[QF@T^A\\G[G_[SGS{VPF]SG[@{UC^F\\@WS[G\\\\AFW[V[@WFFGGWGWSZFSA\\A[\\^GF@WQWF[G[GA^SG[DF]G\\V^sSFC\\\\@QX]W[S^SS][SUAAG][F[DW^]@CD\\AWd[GW@[W^W@Q'),
(9, 3, '1 1 lagi', 'uTJ]KM\\Z\\MXPWUJZJVK\\KV\\]PUKMKP\\MKPVZ]UTVJPOKW^P]\\X]J\\JTT\\XPt\\KXZKJP\\Z\\MWL\\U\\PLPX]JXLZUUJZXLWW\\W}ZVJJ\\LOMMVK]PTQUMVU\\MLTIW\\WM\\JLIVP]VJLXL^J\\VIU\\MPPV\\MLXMOKIPOPU\\PI\\TXPHL}ZWKXJZWJMVVKXWWL_PXUJ\\\\]LK]xLZLPL\\O\\WL\\XPPT^TLKPPL}KJPUXJM\\WMV\\ILVVPTMVJZ\\L]IJP^\\PzXXPPPKX\\TMJ]KML]VTUJXXOM\\WPP\\V\\VMKTATJOOKXW\\\\LJJUPPLPV\\}WZTJXWJIUPXVXPMJPOWWMJPLzX^JX\\IJHX^MPZUJXZWJIX\\KKL\\VPLZIMXMLMJ\\iXJWVJHXUMWUXL_W[JU^UVX\\zK[MKX\\P\\}P\\PTWUX\\\\WX\\LLZV\\QWLLM^MU^UVLIMMIKMMKLWPWJPiX\\UJIKMMK\\PUMPXUXZK\\\\L\\\\XP^M\\M[UTJT\\]VOU\\\\_WQWLJ\\OM\\]P\\\\XPWOUMXXK\\wTJMX\\UMT}WZXWTP\\UJJ^MPP\\KjJ\\]J\\ZWXUJXPLMWJ\\VLKXWKJPLMV\\V^\\IX\\KPUXKX\\LZ\\IKIJ\\\\JI\\VJHXXZ[JQJUL\\IK_UJLPMT^XPXUHXV^\\_W[JJTPXPZ]WAPZUJJMX\\j]_LPM]X]PJTMPMH\\\\_ZMKLJ\\PLKWPUJ]UJTJX\\_K\\MT\\PKPTUJXWMKPZMK_UJWLPLTPXLXp][MVXLPKp^HUMWK\\XPLWWJM\\P]PK\\MMLL\\L\\XQMXJWJPWULMK\\Z\\MPLPLJUXLPOMVLW]UxXMHWWKZSV\\PXUXXVPX^JJLVPMPO\\UVKHOWJ\\oPL\\KP\\U\\KZ3ZPMILMVMXPT\\\\ZP]UPJOXLWJVUHUMJ\\^MM\\WZLQMWVK\\TLPZ\\MLLi\\JTPMZOPTWPMMPMLM\\\\XPPIJL_PPMJ_^XV\\XTLU');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` varchar(150) NOT NULL,
  `passhash` varchar(128) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `passhash`) VALUES
(1, 'estetika', '0c79cdda0b4fca6014a1a171b608f17d4f373bc7f1187c3cf87fcffa490fc638'),
(2, 'kaka', '0c79cdda0b4fca6014a1a171b608f17d4f373bc7f1187c3cf87fcffa490fc638'),
(3, 'user1', 'c3e4d5dfd504f477d3fe386cb7a960ec6de15be90de37a04ea8b2dfbbf33c509');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `notes`
--
ALTER TABLE `notes`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `notes`
--
ALTER TABLE `notes`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `notes`
--
ALTER TABLE `notes`
  ADD CONSTRAINT `notes_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
