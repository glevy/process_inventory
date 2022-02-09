# Deploy Artifact utility

This utility provides an easy way to deploy any given folder as a maven artifact.
Using the benefits of maven as a package manager, you can take advantage of versioning, SNAPSHOTS and better manage your build artifacts.
You can also use it with the Process inventory utility described below to deploy your build environment from Artifactory or build your installation folder tree from the specific version of each component.
This will allow you to build smaller components (microservices), deploy them seperately and then package your product in a central build. 

The artifactory URL and credentials needs to be set in the settings.xml file.

The password tag can contain the user api key.

```
      <properties>
            <deploy-contextUrl>http://artifactory:8081/artifactory</deploy-contextUrl>
            <deploy-username>user</deploy-username>
            <deploy-password>AKCp5fU4WMYj8Z...........................</deploy-password>
        </properties>
```


## Deploying artifacts

Execute:

```bash

python deploy.py --artifactId kuku --version 1.0.14 --groupId deployed.artifacts --deployRepository local-lib-Corporate_Dev --sourcePath C:\Temp\deploy-test

usage: deploy.py [-h] [--artifactId ARTIFACTID] [--version VERSION]
                 [--groupId GROUPID] [--sourcePath SOURCEPATH]
                 [--deployRepository DEPLOYREPOSITORY]

This program will deploy an artifact using maven

optional arguments:
  -h, --help            show this help message and exit
  --artifactId ARTIFACTID
                        the artifact name
  --version VERSION     the artifact version
  --groupId GROUPID     the artifact groupId (path in artifactory)
  --sourcePath SOURCEPATH
                        the artifact source path (the folder that contains the
                        artifact content)
  --deployRepository DEPLOYREPOSITORY
                        the artifactory repository name into which the
                        artifact will be deployed
```


----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------------------------

# Process inventory utility

This utility provides an easy and trackable way to downlodad and build a project dependency tree using Maven.
It can be used with any technology and build tool.

It expects a csv file that lists the required artifacts and the target path to unpack them `inventory.csv`.
The `csv` format was chosen for the ease of use and the ability to edit it with MS Excell.

An example for inventory.csv content (the first row is being ignored by the tool)
```
artifactId, version, groupId, targetPath
kuku, 1.0.0, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.0\
kuku, 1.0.1, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.1\
kuku, 1.0.2, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.2\
kuku, 1.0.3, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.3\
kuku, 1.0.4, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.4\
kuku, 1.0.5, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.5\
kuku, 1.0.6, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.6\
kuku, 1.0.7, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\1.0.7\
kuku, LATEST, deployed.artifacts, c:\temp\process_inventory\deployed_artifacts\latest\
```
The source maven repositories can be configured in `settings.xml`.


## Unpacking artifacts

Execute:

```bash
python process_inventory.py -i <path to inventory.csv>

usage: process_inventory.py [-h] [--inventory INVENTORY]

This program will process an artifact inventory file and extract each artifact
to the specified target folder

optional arguments:
  -h, --help            show this help message and exit
  --inventory INVENTORY, -i INVENTORY
                        The path to the inventory file (.csv)
```
