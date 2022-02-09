import csv
import os
import sys
import argparse


deployRepository = "local-lib-Corporate_Dev"

parser = argparse.ArgumentParser(description="This program will deploy an artifact using maven")
parser.add_argument('--artifactId', type=str, help='the artifact name')
parser.add_argument('--version', type=str, help='the artifact version')
parser.add_argument('--groupId', type=str, help='the artifact groupId (path in artifactory)')
parser.add_argument('--sourcePath', type=str, help='the artifact source path (the folder that contains the artifact content)')
parser.add_argument('--deployRepository', type=str, help='the artifactory repository name into which the artifact will be deployed')

args = parser.parse_args()
if not args.artifactId or not args.groupId or not args.version or not args.sourcePath:
    print("\nError:", "please provide all the required arguments!\n")
    parser.print_help()
    sys.exit()
    
if args.deployRepository is not None:
    deployRepository = args.deployRepository

pom_file = "deploy_pom.xml"
pom_template = """
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>
  <groupId>{groupId}</groupId>
  <artifactId>{artifactId}</artifactId>
  <version>{version}</version>
  <packaging>pom</packaging>
	<build>
	<plugins>
		<plugin>
		    <groupId>org.apache.maven.plugins</groupId>
			<artifactId>maven-assembly-plugin</artifactId>
			<version>3.0.0</version>
			<configuration>
				<descriptors>
					<descriptor>./zip.xml</descriptor>
				</descriptors>
				<packaging>zip</packaging>
			<appendAssemblyId>false</appendAssemblyId>
			</configuration>
			<executions>
			  <execution>
				<id>create-distribution</id>
				<phase>clean</phase>
				<goals>
				  <goal>single</goal>
				</goals>
			  </execution>
			</executions>
			</plugin>
            <plugin>
            <groupId>org.jfrog.buildinfo</groupId>
            <artifactId>artifactory-maven-plugin</artifactId>
            <version>3.0.0</version>
            <inherited>false</inherited>
            <executions>
                <execution>
                    <id>build-info</id>
                    <goals>
                        <goal>publish</goal>
                    </goals>
                    <configuration>
                        <deployProperties>
                            <gradle>awesome</gradle>
                            <review.team>qa</review.team>
                        </deployProperties>
                        <publisher>
                            <publishBuildInfo>false</publishBuildInfo>
                            <repoKey>{deployRepository}</repoKey>
                            <snapshotRepoKey>{deployRepository}</snapshotRepoKey>
                            <contextUrl>${{deploy-contextUrl}}</contextUrl>
                            <username>${{deploy-username}}</username>
                            <password>${{deploy-password}}</password>    
                        </publisher>
                    </configuration>
                </execution>
            </executions>
        </plugin>
		</plugins>
	  </build>
</project>
"""
pom = open(pom_file, 'w')
pom.write(pom_template.format(artifactId=args.artifactId, version=args.version, groupId=args.groupId, sourcePath=args.sourcePath,deployRepository=deployRepository))
pom.close()
path = os.path.dirname(os.path.realpath(__file__))
os.system("mvn clean deploy -f {} -Ddeploy.name={} -Ddeploy.version={} -Ddeploy.dir={} -s {}/settings.xml".format(pom_file,args.artifactId,args.version,args.sourcePath,path))
