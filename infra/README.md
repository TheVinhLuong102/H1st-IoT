# Predictive Maintenance Infrastructure

Directory structure:

  * `aws`: 
    * Terraform infrastructure module for PM environment and yarn clusters.
  * `bai`: BAI setup and config manifest file.
    * Note: `bai/cluster-bai-ccpm/terraform` is managed by BAI installer. Do not edit these files directly.
    * To provision: run `h1st_installer.run setup`
    * To install: cd to cluster folder and run 
      * `h1st_install.run install --hosts aux_worker,api_server --debug`

How to deploy new version to CCPM:

  * Go to jenkins -> PENG -> build docker. Set tag name to sprint release with SNAPSHOT
  * Go to jenkins -> bai-installer -> publish. Change VERSION and PENG_TAG to the same version as in before.
  * Update setup.yaml with the right version. **Use h1st_installer**  to run setup to regenerate the config.yaml
  * **Use h1st_installer**  to install the host: api_server,aux_worker,etl_worker

How to update new dependencies of YARN cluster:

  * Make sure to setup the terraform workspace under `infra/aws` using `terraform init`
  * Update the provision script s3://h1st-bai-clusters/custom_provisioner/ccpm/yarn-deps.sh
  * Update `cluster_version` in the `yarns.tf`
  * Run terraform plan & apply. It's better to use `-target` to plan only for the cluster.
