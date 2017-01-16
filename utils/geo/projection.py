from __future__ import print_function
from __future__ import print_function
from pyproj import Proj

long_lat_proj = Proj(proj='longlat', ells='WGS84', datum='WGS84', no_defs=True)
merc_proj = Proj(proj='merc', a=6378137, b=6378137, lat_ts=0.0, lon_0=0.0, x_0=0.0, y_0=0, k=1.0, units='m', nadgrids='@null', no_defs=True)

coords = 48, 11
print(long_lat_proj(*coords))
print(merc_proj(*coords))

# +proj=longlat +ellps=WGS84 +datum=WGS84 +no_defs

# +proj=merc +a=6378137 +b=6378137 +lat_ts=0.0 +lon_0=0.0 +x_0=0.0 +y_0=0 +k=1.0 +units=m +nadgrids=@null +no_defs