import pandas as pd
from functions.functions import pfm_check, buoy_check, node_check
import re


def main(f, ref_des, stream, method, pd_number):
	# read in data
	csv_file = open(f, 'r')
	data = pd.read_csv(csv_file, parse_dates=True)

	# reduce data frame to relevant columns
	columns = ['reference_designator','start_depth','end_depth','method','stream_name', 'parameter_id',
								'name.1','parameter_function_map', 'data_product_identifier', 'data_level']
	data = data[columns]

	# stage list of expected PD numbers to br printed from at end of script
	affected_PDs = []

	# create regular expression to enter buoy exception and search across nodes
	buoy_nodes = ['RID', 'SBD']
	reg_ex = re.compile('|'.join(buoy_nodes))

	# further reduce data frame to only those instruments that might be affected
	if reg_ex.search(ref_des):
		possible_instruments = buoy_check(data, ref_des, method)
	else:
		possible_instruments = node_check(data, ref_des, method)

	# begin recursive search on reduced data frame
	pfm_check(possible_instruments, pd_number, affected_PDs)
	affected_PDs = set(affected_PDs)

	# print output
	print '\n' + pd_number + ' from ' + ref_des + '-' + stream + ' is to calculate:\n'
	for i in affected_PDs:
		print i
	print '\n'

if __name__ == '__main__':
	# define your inputs
	f = '/Users/knuth/Documents/ooi/repos/github/annotations/tools/pfm/all_params.csv'

	# ref_des = 'RS03AXPS-PC03A-4A-CTDPFA303'
	# stream = 'ctdpf_optode_sample'
	# method = 'streamed' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD194'

	# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	# stream = 'ctdbp_cdef_instrument_recovered'
	# method = 'recovered_inst' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD923'

	ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	stream = 'ctdbp_cdef_dcl_instrument'
	method = 'telemetered' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	pd_number = 'PD923'

	# ref_des = 'CE02SHSM-RID27-03-CTDBPC000'
	# stream = 'ctdbp_cdef_dcl_instrument_recovered'
	# method = 'recovered_host' # 'recovered_host' 'telemetered' 'recovered_inst' 'recovered_cspp' 'streamed' 'recovered_wfp'
	# pd_number = 'PD923'
	main(f, ref_des, stream, method, pd_number)




