import csv
import os, sys
import argparse



parser = argparse.ArgumentParser(description="This program will process an artifact inventory file and extract each artifact to the specified target folder")
parser.add_argument('--inventory', '-i', type=str, help='The path to the inventory file (.csv)')

args = parser.parse_args()

if args.inventory is not None:
    inventory_file = args.inventory
else:
    print("\nError:","please provide the path to the inventory file!\n")
    parser.print_help()
    sys.exit()
    
pom_file = "inventory_pom.xml"
pom_template = """
<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    <groupId>Artifactory</groupId>
    <artifactId>Downloader</artifactId>
    <version>1.0-SNAPSHOT</version>
	<build>
        <plugins>
            <plugin>
                <groupId>org.apache.maven.plugins</groupId>
                <artifactId>maven-dependency-plugin</artifactId>
                <executions>
                    <execution>
                        <id>unpack-include</id>
                        <phase>generate-sources</phase>
                        <goals>
                            <goal>unpack</goal>
                        </goals>
                    </execution>
				</executions>
				<configuration>
					<artifactItems>
						 {artifactItems}
					</artifactItems>
                    <overWriteSnapshots>true</overWriteSnapshots>
				    <overWriteReleases>true</overWriteReleases> 
				</configuration>
			</plugin>
		</plugins>
	</build>
</project>
"""
artifact_items = []
with open(inventory_file, newline='') as inventory:
    inventory_reader = csv.reader(inventory, delimiter=',', skipinitialspace=True, quotechar='|')
    next(inventory_reader)

    for row in inventory_reader:
        artifact_item = """<artifactItem>
                            <artifactId>{}</artifactId>
                            <version>{}</version>
							<groupId>{}</groupId>
		                    <type>zip</type>
                            <outputDirectory>{}</outputDirectory>                     
						</artifactItem>""".format(*row)
        artifact_items.append(artifact_item)

pom = open(pom_file, 'w')
pom.write(pom_template.format(artifactItems='\n					    '.join(artifact_items)))
pom.close()
path = os.path.dirname(os.path.realpath(__file__))
print("Running: mvn -B -U dependency:unpack -f {pom} -s {path}/settings.xml".format(pom=pom_file,path=path))
os.system("mvn -B -U dependency:unpack -f {pom} -s {path}/settings.xml".format(pom=pom_file,path=path))