resource "oci_core_instance" "VM-Developer" {

    
    availability_domain     = data.oci_identity_availability_domain.ad.name
    compartment_id          = var.compartment_ocid
    shape                   = var.vm_shape
    display_name            = "VM-Developer"
    preserve_boot_volume    = false

    create_vnic_details {
        assign_public_ip    = var.vm_public
        subnet_id           = oci_core_subnet.publicsubnet1.id
    }

    # shape_config {
    #     memory_in_gbs   = "1"
    #     ocpus           = "1"
    # }
    metadata = {
        ssh_authorized_keys = var.ssh_public_key
    }
    
    source_details {
        source_id = data.oci_core_images.vm-images.images[0]["id"]
        source_type = "image"
    }
}

output "vm_ip" {
    value = oci_core_instance.VM-Developer.public_ip
}
output "vm_public" {
    value = var.vm_public
}
