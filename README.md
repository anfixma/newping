# newping
Ping stats tool for The Open Technology Institute as initial contributing as part of Outreachy program

Newping is a script that automaticaly runs a network (ping) test at regular intervals
and and creates a graph based on collected metrics.
It uses `cron` to run test task.
For now it saves metrics to files, one per day and displays statistic
for the given day only.

See INSTALL for installation recommendations.


## Config
You can add your own "ping-points" to `ip.json` config file. By default there are
a few root DNS servers from two regions: US and EU.

Check interval could be changed in crontab.

## Dependencies:
* pygal
* pyping
* pycairo
