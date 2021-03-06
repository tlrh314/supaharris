import os
import sys
import numpy
import logging
from matplotlib import pyplot
from astroquery.vizier import Vizier
Vizier.ROW_LIMIT = -1

BASEDIR = "/".join(__file__.split("/")[:-1]) + "/MW_GCS_Trager1995/"


def fix_gc_names(data):
    for i, n in enumerate(data["Name"]):
        data["Name"][i] = n.replace("ngc", "NGC ").replace("arp", "Arp "
        ).replace("hp", "HP").replace("ic", "IC ").replace("terzan", "Terzan "
        ).replace("ton", "Ton ").replace("pal_", "Pal ").replace("am1", "AM 1")
        # ReadMe: "Note on Name: hp stands for HP 1, <Cl Haute-Provence 1> in Simbad"
        if n.strip().lower() == "hp":
            data["Name"][i] = "HP 1"
    return data


def parse_trager_1995_gc(logger, fname="{0}Vizier_gc.txt".format(BASEDIR), refetch=False):
    # This table was added by CDS, but does not actually contain relevant information

    if os.path.exists(fname) and os.path.isfile(fname) and not refetch:
        dtype = [
            ("Name", "<U8"), ("Nsb", "<i2"), ("SName", "<U19"), ("Prof", "<U4"),
            ("Simbad", "<U6"), ("_RA", "<f8"), ("_DE", "<f8")
        ]
        return fix_gc_names(
            numpy.loadtxt(fname, dtype=dtype, delimiter=",")
        )

    table = Vizier.get_catalogs("J/AJ/109/218/gc")[0]
    table.convert_bytestring_to_unicode()  # to remove b'' from string columns
    data = fix_gc_names(numpy.array(table))  # Numpy structured array
    print("bla", data["Name"])
    numpy.savetxt(fname, data, header=", ".join(data.dtype.names),
        fmt=",".join(["%s"]*len(data.dtype)))
    return data


def parse_trager_1995_tables(logger, fname="{0}Vizier_tables.txt".format(BASEDIR), refetch=False):
    if os.path.exists(fname) and os.path.isfile(fname) and not refetch:
        dtype = [
            ("Name", "<U8"), ("logr", "<f4"), ("muV", "<f4"), ("muVf", "<f4"),
            ("Resid", "<f4"), ("Weight", "<f4"), ("DataSet", "<U9")
        ]
        return fix_gc_names(
            numpy.loadtxt(fname, dtype=dtype, delimiter=",")
        )

    # Byte-by-byte Description of file: tables.dat
    # --------------------------------------------------------------------------------
    #    Bytes Format Units      Label    Explanations
    # --------------------------------------------------------------------------------
    #    1-  8  A8    ---        Name    *Cluster name
    #   10- 15  F6.3 [arcsec]    logr     Log of radius of surface brightness meas.
    #   18- 22  F5.2 mag/arcsec2 muV      Meas. surface brightness at r, in V mags.
    #   25- 29  F5.2 mag/arcsec2 muVf     Fitted surface brightness at r, from
    #                                      Chebyshev fit
    #   31- 36  F6.2 mag/arcsec2 Resid    Residual of Chebyshev fit at r, muV-muVf
    #   40- 44  F5.3 ---         Weight   [0/1] Weight of data point in Chebyshev fit
    #   47- 55  A9   ---         DataSet *Data set name

    table = Vizier.get_catalogs("J/AJ/109/218/tables")[0]
    table.convert_bytestring_to_unicode()  # to remove b'' from string columns
    data = numpy.array(table)  # Numpy structured array
    data = fix_gc_names(data)
    numpy.savetxt(fname, data, header=", ".join(data.dtype.names),
        fmt=",".join(["%s"]*len(data.dtype)))
    return data


def parse_trager_1995_chebyshev_fits(logger, fname="{0}tables.hdr".format(BASEDIR)):
    with open(fname) as f:
        raw_data = f.readlines()

    logger.debug("\n\n{0} contains {1} rows\n\n".format(fname, len(raw_data)))


def plot_trager_1995_surface_brightness_profile(logger, tables, gc_name):
    igc, = numpy.where(tables["Name"] == gc_name)

    logger.info("{0} has {1} entries".format(gc_name, len(tables[igc])))
    ikeep = Ellipsis
    if gc_name == "NGC 2419":  # the data shows two radial profiles
        ikeep, = numpy.where(
            (tables[igc]["DataSet"] != "CGB1")
            & (tables[igc]["DataSet"] != "CGB2")
            & (tables[igc]["DataSet"] != "CGR1")
            & (tables[igc]["DataSet"] != "CGR2")
            & (tables[igc]["DataSet"] != "CGV2")
            & (tables[igc]["DataSet"] != "CGV1")
            & (tables[igc]["DataSet"] != "CGV3")
        )
        # logger.debug(ikeep)
        logger.info("ikeep has {0} entries".format(len(ikeep)))
        # logger.debug(tables[igc]["DataSet"][ikeep])

    fig = pyplot.figure(figsize=(12, 10))
    ax1 = pyplot.axes([(0-1)/2, 0.40, 1.00/2, 0.60 ])  # left, bottom, width, height
    ax2 = pyplot.axes([(0-1)/2, 0.10, 1.00/2, 0.30 ])

    ax1.text(0.98, 0.98, "{0} (T95)".format(gc_name),
        ha="right", va="top", transform=ax1.transAxes, fontsize=16)
    ax1.errorbar(tables[igc]["logr"][ikeep], tables[igc]["muV"][ikeep],
        marker="o", c="k", ls="", ms=4, elinewidth=2, markeredgewidth=2, capsize=5,
        label="data")
    ax1.plot(tables[igc]["logr"][ikeep], tables[igc]["muVf"][ikeep], "ro", ms=5,
        label="Chebyshev fit")
    ax1.set_ylabel("$\mu_V$ [mag/arcsec$^2$]")
    ax1.set_xticks([], [])
    ax1.invert_yaxis()
    ax1.legend(loc="lower left", frameon=False, fontsize=16)

    ax2.plot(tables[igc]["logr"][ikeep], tables[igc]["Resid"][ikeep], "ko", ms=4)
    ax2.axhline(0, c="k", lw=2, ls=":")
    ax2.set_xlabel("$\log(r)$ [arcsec]")
    ax2.set_ylabel("Residuals")
    ymin, ymax = ax2.get_ylim()
    ylim = max(abs(ymin), abs(ymax))
    ax2.set_ylim(-ylim, ylim)
    fig.subplots_adjust(wspace=0, hspace=-0.02, left=0.03, right=0.97, bottom=0.02, top=0.98)

    return fig


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__name__)
    logger.info("Running {0}".format(__file__))

    gc = parse_trager_1995_gc(logger)
    gc_simbad = parse_trager_1995_gc(logger, refetch=True)
    assert len(gc) == len(gc_simbad)
    assert gc.dtype == gc_simbad.dtype
    for i in range(len(gc)):
        assert gc[i] == gc_simbad[i], "Mismatch\n{0}\n{1}".format(gc[i], gc_simbad[i])
    logger.debug("\ngc has {0} entries".format(len(gc)))
    logger.debug("dtype: {0}".format(gc.dtype))

    tables = parse_trager_1995_tables(logger)
    tables_simbad = parse_trager_1995_tables(logger, refetch=True)
    assert len(tables) == len(tables_simbad)
    assert tables.dtype == tables_simbad.dtype
    for i in range(len(tables)):
        assert tables[i] == tables_simbad[i]
    logger.debug("\ntables has {0} entries".format(len(tables)))
    logger.debug("dtype: {0}".format(tables.dtype))

    parse_trager_1995_chebyshev_fits(logger)

    clusters = gc["Name"]
    for i, gc_name in enumerate(clusters):
        fig = plot_trager_1995_surface_brightness_profile(logger, tables, gc_name)
        pyplot.savefig("data/MW_GCS_Trager1995/Trager1995_SurfaceBrightness_{0}.pdf".format(gc_name))
        pyplot.close(fig)
        break
