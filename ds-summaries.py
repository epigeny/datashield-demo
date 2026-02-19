import logging
from datashield import DSSession, DSLoginBuilder

logging.basicConfig(level=logging.INFO)

server_names = ["server1"] #, "server2", "server3"]
logins = DSLoginBuilder(names = server_names).build()

session = DSSession(logins)
session.open()

try:
    session.assign_table("df", tables={"server1": "CNSIM.CNSIM1", "server2": "CNSIM.CNSIM2", "server3": "CNSIM.CNSIM3"})

    all_colnames = session.aggregate('colnamesDS("df")')
    logging.info(all_colnames)

    # List the colunames in common across all servers
    common_colnames = set(all_colnames["server1"])
    for server in all_colnames:
        common_colnames = common_colnames.intersection(set(all_colnames[server]))
    logging.info(common_colnames)

    # Get the summary of each column in the common columns
    for colname in common_colnames:
        logging.info(f"Summary of column {colname}:")
        col_class = session.aggregate(f'classDS(df${colname})')
        logging.info(f"Class of column {colname}: {col_class}")
        col_is_factor = session.aggregate(f'is.factor(df${colname})')
        logging.info(f"Is column {colname} a factor? {col_is_factor}")
        if col_class["server1"] in ["numeric", "integer"]:
            if col_is_factor["server1"]:
                levels = session.aggregate(f'levelsDS(df${colname})')
                logging.info(f"Levels of column {colname}: {levels}")
                summary = session.aggregate(f'tableDS(df${colname}, force.nfilter.transmit = NULL, rvar.all.unique.levels.transmit = "1,2,3", cvar.transmit = NULL, stvar.transmit = NULL, exclude.transmit = NULL)')
            else:
                summary = session.aggregate(f'meanDS(df${colname})')
            logging.info(f"Summary of column {colname}: {summary}")
        logging.info(summary)
except Exception as e:
    logging.error(f"An error occurred: {e}")
    if session.has_errors():
        logging.error(session.get_errors())
finally:
    session.close()