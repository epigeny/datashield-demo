from datashield import DSSession, DSLoginBuilder
import pandas as pd

logins = DSLoginBuilder(names = ["server1", "server2"]).build()

session = DSSession(logins)
session.open()

profiles = session.profiles()
print(profiles)

pkgs = session.packages()
print(pd.DataFrame.from_records(pkgs["server1"]))

methods = session.methods(type="aggregate")
print(pd.DataFrame.from_records(methods["server1"]))

tables = session.tables()
print(tables)

resources = session.resources()
print(resources)

session.close()