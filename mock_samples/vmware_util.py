# author: Petros Petrou
# date: 13/06/2021

from pyVim.connect import SmartConnectNoSSL, Disconnect
from pyVmomi import vim, vmodl

class VmwareOpen(object):

    def __init__(self, host, port, username, password):
        self._host = host
        self._port = port
        self._username = username
        self._password = password

    def __enter__(self):
        try:
            self._service_instance = SmartConnectNoSSL(host=self._host, user=self._username, pwd=self._password, port=self._port)
            return self._service_instance
        except IOError as e:
            raise e

    def __exit__(self, type, value, traceback):
        Disconnect(self._service_instance)

class VmwareUtil(object):
    
    def __init__(self, vmwarehost, vmwareport, username, password):
        self._host = vmwarehost
        self._port = vmwareport
        self._username = username
        self._password = password
    
    def _get_vm(self, identity, service_instance):
        content = service_instance.RetrieveContent()
        
        vmlist = []
        
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'vmFolder'):
                datacenter = child
                vmfolder = datacenter.vmFolder
                vmlist = vmfolder.childEntity
                
        for vm in vmlist:
            if vm.summary.config.name == identity or vm.summary.config.uuid == identity:
                return vm
        
        raise Exception(identity + " not found.")
    
    def get_uuid(self, identity):
        with VmwareOpen(self._host, self._port, self._username, self._password) as service_instance:
            vm = self._get_vm(identity, service_instance)
            return vm.summary.config.uuid
    
def tryme():
    vmware_util = VmwareUtil("192.168.122.168", "443", "root", "root#esxi!80")
    vmuuid = vmware_util.get_uuid("test_vm_00")
    print("UUID : " + vmuuid)

if __name__ == "__main__":
    tryme()
