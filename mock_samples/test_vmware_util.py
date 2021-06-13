# author: Petros Petrou
# date: 13/06/2021

import unittest
from unittest import mock
from unittest.mock import patch

from vmware_util import VmwareUtil

from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl

class TestVMwareUtil(unittest.TestCase):
    
    @mock.patch('vmware_util.VmwareOpen')
    def test_uuid(self, vmware_mock):
        
        # Initialize the Config Summary
        test_vm_00_config_summary = mock.MagicMock(spec_set=vim.vm.Summary.ConfigSummary())
        test_vm_00_config_summary.name = "test_vm_00"
        test_vm_00_config_summary.uuid = "c7a5fdbd-cdaf-9455-926a-d65c16db1809"
         
        # Initialize VM Summary 
        test_vm_00_summary = mock.MagicMock(spec_set=vim.vm.Summary())
        test_vm_00_summary.config = test_vm_00_config_summary
        
        # Initialize the Mock VM
        test_vm_00 = mock.MagicMock(spec_set=vim.VirtualMachine("vm-41"))
        test_vm_00.summary = test_vm_00_summary
        
        # Initialize the Data Center and add the Mock VM
        # Create the vmFolder       
        vm_folder_mock = mock.MagicMock(spec_set=vim.Folder("vm-folder"))
        vm_folder_mock.childType = { "vim.Folder", "vim.Virtualmachine", "vim.VirtualApp" }       
        # Add it to the Data Center and add the VM in the children
        ds_mock = mock.MagicMock(spec_set=vim.Datacenter("ds-00"))
        ds_mock.vmFolder = vm_folder_mock
        ds_mock.vmFolder.childEntity = [test_vm_00]
        
        # Initialize the Service Instance Mock and add the Data Center
        # Create the rootFolder
        root_folder_mock = mock.MagicMock(spec_set=vim.Folder("root-folder"))
        root_folder_mock.childEntity = [ds_mock]
        # Create the Service Instance and add the rootFolder
        si_mock = mock.MagicMock(spec_set=vim.ServiceInstance("si-00"))
        si_content_mock = mock.MagicMock(spec_set=vim.ServiceInstanceContent())
        si_content_mock.rootFolder = root_folder_mock
        # Mock the RetrieveContent Methos in the service instance
        si_mock.RetrieveContent = mock.MagicMock(return_value=si_content_mock)
        #si_mock.RetrieveContent.side_effect = Exception('Boom!')
        
        # Get the VmwareOpen reference
        vm_mock = vmware_mock.return_value
        # Mock the enter and exit methods
        vm_mock.__enter__ = mock.MagicMock(return_value=si_mock)
        vm_mock.__exit__ = mock.MagicMock(return_value=None)
        
        # Call the VMWare Util as normal. Any vmware_util.VmwareOpen reference within the function call will be replaced by the mocked object.
        vmware_util = VmwareUtil("", "", "", "")
        returned_uuid = vmware_util.get_uuid("test_vm_00")
         
        # Assert
        self.assertEqual('c7a5fdbd-cdaf-9455-926a-d65c16db1809', returned_uuid)


if __name__ == '__main__':
    unittest.main()












                