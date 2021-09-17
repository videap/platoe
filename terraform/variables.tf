
variable "compartment_ocid" {}
variable "region" {}
variable "instance_shape" {}
variable "tenancy_ocid" {}
variable "user_ocid" {}
variable "fingerprint" {}
variable "private_key_path" {}
variable "token" {}
variable "ssh_public_key" {}
variable "vm_os"{}
variable "vm_os_version"{}
variable "vm_shape"{}
variable "vm_public"{}
variable "vcn1_cidr"{}
variable "vcn1_dnslabel"{}
variable "ad_number" {}


data "oci_identity_availability_domain" "ad" {
  compartment_id  = var.tenancy_ocid
  ad_number       = var.ad_number
}


data "oci_core_images" "vm-images" {
  compartment_id           = var.compartment_ocid
  operating_system         = var.vm_os
  operating_system_version = var.vm_os_version
  shape                    = var.vm_shape
}