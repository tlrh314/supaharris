import os
import sys
import numpy
import logging
from matplotlib import pyplot


BASEDIR = "/".join(__file__.split("/")[:-1]) + "/MW_GCS_Balbinot2018/"


def fix_gc_names(name):
    from utils import convert_gc_names_from_sh_to_any
    return convert_gc_names_from_sh_to_any(name, reverse=True)  # from deBoer to SH


def parse_balbinot_2018(logger, fname="{0}latex_table_semi_cleaned.txt".format(BASEDIR)):
    with open(fname) as f:
        raw_data = f.readlines()

    # Clean up LaTeX table
    names = []
    values = []
    errors = []
    for i, row in enumerate(raw_data):
        row_values = []
        row_errors = []
        if i == 1: continue   # units

        row = row.replace("\\", "").replace("$", ""
            ).replace("{", "").replace("}", "").replace("*", "")
        columns = row.split("&")
        for j, column in enumerate(columns):
            if i == 0:  # header
                names.append(column.strip())
                continue

            if "pm" in column:
                value, error = column.split("pm")
                value = value.strip()
            else:
                value = column.strip()
                error = numpy.nan
            value = numpy.nan if "--" in value else value
            # Not needed to fix gc names. In fact, the method has bug for
            # 'Eridanus' --> 'Eridanus danus' TODO
            # if j is 0:
            #     value = fix_gc_names(value)

            try:
                value = float(value)
            except ValueError:
                pass
            try:
                error = float(error)
            except ValueError:
                pass

            row_values.append(value)
            row_errors.append(error)

        if i == 0: continue  # header
        values.append(row_values)
        errors.append(row_errors)
        for name, value, error in zip(names, row_values, row_errors):
            if type(value) == float:
                info = "{0:<20s}{1:>10.2f}".format(name, value)
            else:
                info = "{0:<20s}{1:<10s}".format(name, str(value))
            if numpy.isfinite(error):
                info += " +/- {0:<10.2f}".format(error)

            # if i >= 3: logger.debug(info)

    # Now build structured array
    dtype = {"names": [], "formats": []}
    for name in names:
        if name in ["Name", "Refs"]:
            dtype["names"].append(name)
            dtype["formats"].append("U16")
        else:
            dtype["names"].append(name)
            dtype["formats"].append("f8")
            dtype["names"].append(name + "_err")
            dtype["formats"].append("f8")

    data = numpy.empty(len(raw_data)-2, dtype=dtype)
    for i, (row_value, row_error) in enumerate(zip(values, errors)):
        for name, value, error in zip(names, row_value, row_error):
            data[i][name] = value
            if name not in ["Name", "Refs"]:
                data[i][name+"_err"] = error

    return data  # or return names, values, errors

def print_balbinot_2018(logger, data):
    header = "".join(["{0:<18s}".format(name) for name in data.dtype.names if "err" not in name])
    ncols = sum(1 for name in data.dtype.names if "err" not in name)
    logger.info("-"*18*ncols)
    logger.info(header)
    logger.info("-"*18*ncols)
    for row in data:
        info = ""
        for i, name in enumerate(data.dtype.names):
            if "err" not in name:
                value = row[name]
                error = row[name+"_err"] if name+"_err" in data.dtype.names else numpy.nan
                if name == "Refs":  # because cosmetics
                    info += "     {:<5s}".format(" ")

                try:
                    info += "{: >8.2f}".format(value)
                except ValueError:
                    info += "{:<8s}".format(str(value))

                if i == 0: continue  # b/c Name does not have _err

                if numpy.isfinite(error):
                    info += " +/- {:<5.2f}".format(error)
                else:
                    info += "     {:<5s}".format("")

        logger.info(info)
    logger.info("-"*18*ncols)


if __name__ == "__main__":
    logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
    logger = logging.getLogger(__file__)
    logger.info("Running {0}".format(__file__))

    data = parse_balbinot_2018(logger)
    logger.info("\nFound {0} GCs".format(len(data)))
    logger.info("\nAvailable fields:\n{0}".format(data.dtype))
    logger.info("\nAvailable clusters:\n{0}".format(data["Name"]))
    # print_balbinot_2018(logger, data)
