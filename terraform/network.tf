
resource "oci_core_vcn" "vcn1" {
  cidr_blocks    =  var.vcn1_cidr
  dns_label      =  var.vcn1_dnslabel
  compartment_id =  var.compartment_ocid
  display_name   = "vcn1"
}

# resource "oci_core_drg" "drg1" {
#     compartment_id  = var.compartment_ocid
#     display_name    = "DRG1"
# }

# resource "oci_core_drg_attachment" "drg_and_vcn1" {
#     drg_id = oci_core_drg.drg1.id
#     vcn_id = oci_core_vcn.vcn1.id
# }

resource "oci_core_internet_gateway" "igw1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id
    display_name    = "IGW_${oci_core_vcn.vcn1.display_name}"
}

resource "oci_core_nat_gateway" "nat1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id
    display_name    = "NAT1_${oci_core_vcn.vcn1.display_name}"
}


resource "oci_core_route_table" "publicRT1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id
    display_name    = "PublicRT1"

    route_rules {
        network_entity_id   = oci_core_internet_gateway.igw1.id
        destination          = "0.0.0.0/0"
    }
}

resource "oci_core_route_table" "privateRT1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id
    display_name    = "PrivateRT1"

    route_rules {
        network_entity_id   = oci_core_nat_gateway.nat1.id
        destination          = "0.0.0.0/0"
    }
}

resource "oci_core_security_list" "publicSL1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id

    display_name = "PublicSL1"

    ingress_security_rules {
        protocol    = "all"
        source      = "0.0.0.0/0"
    }

    egress_security_rules {
        destination     = "0.0.0.0/0"
        protocol        = "all"
    }
}

resource "oci_core_security_list" "privateSL1" {
    compartment_id  = var.compartment_ocid
    vcn_id          = oci_core_vcn.vcn1.id
    display_name    = "PrivateSL1"

    ingress_security_rules {
        protocol    = "all"
        source      = oci_core_vcn.vcn1.cidr_blocks[0]
    }
    egress_security_rules {
        destination = "0.0.0.0/0"
        protocol    = "all"
    }
}


resource "oci_core_subnet" "publicsubnet1" {
    cidr_block          = "20.0.0.0/24"
    compartment_id      = var.compartment_ocid
    vcn_id              = oci_core_vcn.vcn1.id
    display_name        = "PublicSubnet1"
    route_table_id      = oci_core_route_table.publicRT1.id
    security_list_ids   = [oci_core_security_list.publicSL1.id]
}

resource "oci_core_subnet" "privatesubnet1" {
    cidr_block          = "20.0.1.0/24"
    compartment_id      = var.compartment_ocid
    vcn_id              = oci_core_vcn.vcn1.id
    display_name        = "PrivateSubnet1"
    route_table_id      = oci_core_route_table.privateRT1.id
    security_list_ids   = [oci_core_security_list.privateSL1.id]
}

