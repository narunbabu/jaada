# import segyio
# import numpy as np
# from shutil import copyfile
folder=r'D:\Arun\Blade_project\Petrel Projects\Petrel training data1\fudamental dataset\Petrel Fundamentals course data set\Input_data\Seismic data (time)\\'

filename = folder+'ST8511r92.segy'

folder=r'D:\Arun\Blade_project\Seismic data\\'
filename = folder+'RTM_uncalibrated_DTC.sgy'

# with segyio.open(filename, "r") as segyfile:

#     # Memory map file for faster reading (especially if file is big...)
#     segyfile.mmap()

#     # Print binary header info
#     print(segyfile.bin)
#     print(segyfile.bin[segyio.BinField.Traces])

#     # Read headerword inline for trace 10
#     print(segyfile.header[10][segyio.TraceField.INLINE_3D])

#     # Print inline and crossline axis
#     print('Cross-line range> {}-{}'.format(segyfile.xlines[0],segyfile.xlines[-1]))
#     print('In-line range> {}-{}'.format(segyfile.ilines[0],segyfile.ilines[-1]))

#     # Read data along first xline
#     data = segyfile.xline[segyfile.xlines[10]]

#     # # Read data along last iline
#     # data = segyfile.iline[segyfile.ilines[-1]]

#     # # Read data along 100th time slice
#     # data = segyfile.depth_slice[100]

#     # # Read data cube
#     # data = segyio.tools.cube(filename)

# from PyQt5.QtWidgets import QApplication
# import segyviewlib
# qapp = QApplication([])
# l = segyviewlib.segyviewwidget.SegyViewWidget(filename)
# l.show()