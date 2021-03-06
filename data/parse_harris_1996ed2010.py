import sys
import logging
import numpy as np
import pandas as pd
from astropy import units as u
from astropy.coordinates import SkyCoord

logger = logging.getLogger("console")
logger.logLevel = logging.DEBUG

BASEDIR = "/".join(__file__.split("/")[:-1]) + "/MW_GCS_Harris1996e2010/"


class Cluster(object):
    def __init__(self, logger):
        self.logger = logger

        # General
        self.gid  = ""                         # Cluster identification
        self.name = None                       # Other commonly used cluster name

        # Coordinates
        self.ra                 = None         # Right ascension               (Epoch J2000)
        self.dec                = None         # Declination                   (Epoch J2000)
        self.longitude          = None         # Galactic longitude            (Degrees)
        self.latitude           = None         # Galactic latitude             (Degrees)
        self.dist_from_sun      = None         # Distance from sum             (kpc)
        self.dist_from_gal_cen  = None         # Distance from galactic center (kpc)
        self.X                  = None         # Galactic distance component X (kpc)
        self.Y                  = None         # Galactic distance component Y (kpc)
        self.Z                  = None         # Galactic distance component Z (kpc)

        # Metallicity
        self.metallicity        = None         # Metallicity [Fe/H]
        self.w_mean_met         = None         # Weight of mean metallicity

        # Photometry
        self.eb_v               = None         # Foreground reddening, E(B-V)
        self.v_hb               = None         # V magnitude level of the HB, V_HB
        self.app_vd_mod         = None         # Apparent visual distance modulus, (m-M)V
        self.v_t                = None         # Integrated V magnitude, V_t
        self.m_v_t              = None         # Cluster luminosity, M_V,t = V_t - (m-M)V
        self.ph_u_b             = None         # U-B
        self.ph_b_v             = None         # B-V
        self.ph_v_r             = None         # V-R
        self.ph_v_i             = None         # V-i
        self.spt                = ""           # Spectral type
        self.ellipticity        = None         # Projected ellipticity of isophotes, e = 1-(b/a)

        # Velocities
        self.v_r                = None         # Heliocentric radial velocity (km/s)
        self.v_r_err            = None         # Observational uncertainty in radial velocity
        self.c_LSR              = None         # Radial velocity relative to solar neighbourhood
        self.sig_v              = None         # Central velocity dispersion (km/s)
        self.sig_v_err          = None         # Observational uncertainty in velocity dispersion

        # Structural parameters
        self.sp_c               = None         # King-model central concentration, c=log(r_t/r_c)
        self.sp_r_c             = None         # Core radius (arcmin)
        self.sp_r_h             = None         # Half-light radius (arcmin)
        self.sp_mu_V            = None         # Central surface brightness (V magnitudes per arcsec^2)
        self.sp_rho_0           = None         # Central luminosity density, log_10(solar_lum/pc^3)
        self.sp_lg_tc           = None         # Core relaxation time t(r_c) in log_10(yr)
        self.sp_lg_th           = None         # Mean relaxation time t(r_h) in log_10(yr)

    def fill_in(self, do):
        if self.name:
            do.name = self.name

        if self.ra:
            do.ra  = self.ra
            do.dec = self.dec

        if self.longitude:
            do.gallon = self.longitude
            do.gallat  = self.latitude

        if self.dist_from_sun:
            do.dfs = self.dist_from_sun
        if self.dist_from_gal_cen:
            do.dfgc = self.dist_from_gal_cen
        do.x_helio = self.X
        do.y_helio = self.Y
        do.z_helio = self.Z

        if self.metallicity:
            do.metallicity = self.metallicity

        if self.eb_v:
            do.ebv = self.eb_v
        if self.v_t:
            do.MVt = self.v_t
        if self.m_v_t:
            do.L = self.m_v_t
        if self.ellipticity:
            do.ellipticity = self.ellipticity

        if self.v_r:
            do.v_r = self.v_r
            do.ev_r = self.v_r_err
        if self.sig_v:
            do.sig_v = self.sig_v
            do.esig_v = self.sig_v_err

        if self.sp_c:
            do.c = self.sp_c
        if self.sp_r_c:
            do.r_c = self.sp_r_c
        if self.sp_r_h:
            do.r_h = self.sp_r_h
        if self.sp_mu_V:
            do.muV = self.sp_mu_V


def parse_harris1996ed2010(logger, debug=False, save_as_xlsx=False):
    if debug:
        logger.debug("\nParsing Harris 1996, 2010 ed.\n")
    cluster_list = {}

    def read_float(s):
        try:
            val = float(s.strip())
        except:
            val = None
        return val

    def read_str(s):
        s = s.strip()
        return None if s == "" else s


    df = pd.DataFrame(columns=["cname", "altname", "RA", "Dec", "L", "B", "R_Sun",
                               "r_c", "r_h", "c", "[Fe/H]", "E(B-V)", "sig_v",
                               "esig_v", "ellip", "mu_V", "V_r", "eV_r",
                               "V_t"])

    # Ruler for f1
    #0         1         2         3         4         5         6         7         8         9         100
    #01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
    # NGC 104    47 Tuc       00 24 05.67  -72 04 52.6   305.89  -44.89    4.5   7.4   1.9  -2.6  -3.1

    # Parsing first file

    f1 = open(BASEDIR+"/f1.dat")
    df1 = pd.DataFrame(columns=["cname", "altname", "RA", "Dec", "L", "B", "R_Sun"])

    for line in f1:
        c = Cluster(logger)
        c.gid               = line[:12].strip()
        c.name              = read_str(line[12:25])
        ra_str              = read_str(line[25:38])
        dec_str             = read_str(line[38:50])
        c.longitude         = read_float(line[50:58])
        c.latitude          = read_float(line[58:66])
        c.dist_from_sun     = read_float(line[66:73])
        c.dist_from_gal_cen = read_float(line[73:79])
        c.X                 = read_float(line[79:85])
        c.Y                 = read_float(line[85:91])
        c.Z                 = read_float(line[91:])

        coo = SkyCoord(ra=ra_str, dec=dec_str, unit=(u.hourangle, u.degree))
        c.ra = np.round(coo.ra.deg,4)
        c.dec = np.round(coo.dec.deg,4)

        df1.loc[c.gid] = pd.Series({"cname": c.gid,
                                   "altname": c.name,
                                   "RA": c.ra,
                                   "Dec": c.dec,
                                   "L": c.longitude,
                                   "B": c.latitude,
                                   "R_Sun": c.dist_from_sun,
                                   })


        cluster_list[c.gid] = c

    f1.close()


    # Ruler for f2
    #0         1         2         3         4         5         6         7         8         9         100
    #01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
    # NGC 104     -0.72 10   0.04 14.06 13.37  3.95  -9.42   0.37  0.88  0.53  1.14  G4    0.09

    # Now parsing second file
    f2 = open(BASEDIR+"f2.dat")
    df2 = pd.DataFrame(columns=["[Fe/H]", "E(B-V)", "ellip", "V_t"])
    for line in f2:
        gid = line[:12].strip()
        c = cluster_list[gid]
        c.metallicity = read_float(line[13:18])
        c.w_mean_met  = read_float(line[18:21])
        c.eb_v        = read_float(line[21:28])
        c.v_hb        = read_float(line[28:34])
        c.app_vd_mod  = read_float(line[34:40])
        c.v_t         = read_float(line[40:46])
        c.m_v_t       = read_float(line[46:53])
        c.ph_u_b      = read_float(line[53:60])
        c.ph_b_v      = read_float(line[60:66])
        c.ph_v_r      = read_float(line[66:72])
        c.ph_v_i      = read_float(line[72:78])
        c.spt         = read_str(line[78:82])
        c.ellipticity = read_float(line[82:])

        df2.loc[gid] = pd.Series({"[Fe/H]": c.metallicity,
                                 "E(B-V)": c.eb_v,
                                 "V_t": c.v_t,
                                 "ellip": c.ellipticity,
                                 })
    f2.close()


    # Ruler for f3
    #0         1         2         3         4         5         6         7         8         9         100
    #01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
    # NGC 104      -18.0   0.1   -26.7    11.0   0.3   2.07      0.36  3.17   14.38   4.88   7.84  9.55

    f3 = open(BASEDIR+"f3.dat")
    df3 = pd.DataFrame(columns=["r_c", "r_h", "c", "sig_v", "esig_v", "mu_V", "V_r", "eV_r"])
    for line in f3:
        gid = line[:12].strip()
        c = cluster_list[gid]

        c.v_r       = read_float(line[12:19])
        c.v_r_err   = read_float(line[19:25])
        c.c_LSR     = read_float(line[25:33])
        c.sig_v     = read_float(line[33:41])
        c.sig_err   = read_float(line[41:47])
        c.sp_c         = read_float(line[47:54])
        c.sp_r_c       = read_float(line[54:64])
        c.sp_r_h       = read_float(line[64:70])
        c.sp_mu_V      = read_float(line[70:78])
        c.rho_0     = read_float(line[78:85])
        c.lg_tc     = read_float(line[85:92])
        c.lg_th     = read_float(line[92:])

        df3.loc[gid] = pd.Series({"V_r": c.v_r,
                                 "eV_r": c.v_r_err,
                                 "sig_v": c.sig_v,
                                 "esig_v": c.sig_v_err,
                                 "c": c.sp_c,
                                 "r_c": c.sp_r_c,
                                 "r_h": c.sp_r_h,
                                 "mu_V": c.sp_mu_V,
                                 })
    f3.close()

    df = pd.concat([df1, df2, df3], axis=1)
    if save_as_xlsx:
        try:
            import openpyxl
            writer = pd.ExcelWriter("output.xlsx")
            df.to_excel(writer, "Harris")
            writer.save()
        except ImportError:
            logger.error("ERROR: Use 'pip install openpyxl' to save Harris data to xlsx")
            do_continue = input("Press any key to continue...")
    if debug:
        logger.debug(df)

    return cluster_list


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__file__)
    logger.info("Running {0}".format(__file__))

    cluster_list = parse_harris1996ed2010(logger, debug=True, save_as_xlsx=False)
