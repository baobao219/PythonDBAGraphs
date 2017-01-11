"""
PythonDBAGraphs: Graphs to help with Oracle Database Tuning
Copyright (C) 2016  Robert Taft Durrett (Bobby Durrett)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Contact:

bobby@bobbydurrettdba.com

segstat.py

Segment usage statistics for one segment

"""

import myplot
import util

def segstat(owner,object_name,subobject_name,object_type):
    q_string = """
select 
to_char(sn.END_INTERVAL_TIME,'MM-DD HH24:MI') DATE_TIME,
ss.LOGICAL_READS_DELTA,
ss.DB_BLOCK_CHANGES_DELTA
from DBA_HIST_SEG_STAT ss,DBA_HIST_SNAPSHOT sn,DBA_HIST_SEG_STAT_OBJ so
where 
so.OWNER='""" 
    q_string += owner
    q_string += """' and
so.OBJECT_NAME='""" 
    q_string += object_name
    q_string += """' and
so.SUBOBJECT_NAME""" 
    if subobject_name == None:
       q_string += ' IS NULL'
    else:
       q_string += " = '"+subobject_name+"'"
    q_string += """ and
so.OBJECT_TYPE='""" 
    q_string += object_type
    q_string += """' and
so.DBID = ss.DBID and
so.TS# = ss.TS# and
so.OBJ# = ss.OBJ# and
so.DATAOBJ# = ss.DATAOBJ# and
ss.snap_id=sn.snap_id and
ss.INSTANCE_NUMBER=sn.INSTANCE_NUMBER
order by ss.snap_id"""
    return q_string

database,dbconnection = util.script_startup('Usage statistics for one segment')

# Get user input

owner=util.input_with_default('OWNER','SYS')
object_name=util.input_with_default('OBJECT_NAME','OBJ$')

subobject_name=util.input_with_default('SUBOBJECT_NAME','')
if subobject_name == '':
    subobject_name = None
    
object_type=util.input_with_default('OBJECT_TYPE','TABLE')

q = segstat(owner,object_name,subobject_name,object_type);

r = dbconnection.run_return_flipped_results(q)

util.exit_no_results(r)

# plot query
    
# Matplotlib can't seem to handle $$ in the title so replace with xx

myplot.title = ("Segment "+owner+"."+object_name+" on "+database+" database").replace("$$","xx")
myplot.ylabel1 = "Logical Reads"
myplot.ylabel2 = "Block Changes"

myplot.xlabels = r[0]
myplot.ylists = r[1:]

myplot.line_2subplots()