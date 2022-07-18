from constructs import Construct
from aws_cdk import (
    Duration,
    Stack,
    aws_rds as rds,
    aws_ec2 as ec2,
    aws_secretsmanager    as secretsmanager,
    Duration,
    RemovalPolicy
)

class AuroraServerlessStack(Stack):

    def __init__(self, scope:Construct, 
        identifier:str,
        environment:str,
        vpc_id:str,
        data_subnet_ids:list,
        instance_type = None,
        replica_instances:int = 2,
        aurora_cluster_username:str="master",
        backup_retention_days:int=14,
        backup_window:str="00:15-01:15",
        preferred_maintenance_window:str="Sun:23:45-Mon:00:15",
        engine:str="postgresql",    ## Aurora Database Engine: postgresql or mysql
        enable_babelfish:bool=True,
        **kwargs ) -> None:

        super().__init__(scope, identifier, **kwargs)

        ## getting VPC using the ID
        vpc = ec2.Vpc.from_lookup(self, "ExistingVPC", vpc_id=vpc_id, region="us-east-1")

        subnets = list()

        for subnet_id in data_subnet_ids:
            subnets.append(ec2.Subnet.from_subnet_attributes(self, subnet_id.replace("-", "").replace("_", "").replace(" ", ""), subnet_id=subnet_id))

        vpc_subnets = ec2.SubnetSelection(subnets=subnets)

        db_subnet_group = rds.SubnetGroup(self,
            id = "DatabaseSubnetGroup",
            vpc = vpc,
            description = str(identifier) + " subnet group",
            vpc_subnets = vpc_subnets,
            subnet_group_name=identifier
        )

        # creating a security group
        db_security_group = ec2.SecurityGroup(self, "DatabaseSecurityGroup",
             vpc = vpc,
             allow_all_outbound = True,
             description = identifier,
             security_group_name = identifier,
           )

        # adding the ingress rule for postgress port
        db_security_group.add_ingress_rule(
            peer =ec2.Peer.ipv4(vpc.vpc_cidr_block),
            connection =ec2.Port(protocol=ec2.Protocol("TCP"), from_port=5432, to_port=5432, string_representation="tcp5432 Postgresql"),
            description="Access through vpc"
        )

        # parameter group configuration
        parameters = {}
        if enable_babelfish:
            parameters["rds.babelfish_status"] = "on"

        parametergroup = rds.ParameterGroup(
            self,
            id=identifier,
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_13_6), # supports serverless 2
            description="Auora Serverless parameter group managed by CDK",
            parameters = parameters
        )

        # generating rds secrets
        aurora_cluster_secret = secretsmanager.Secret(self, "AuroraClusterCredentials",
            secret_name ="/"+str(environment)+"/"+str(identifier)+"/credentials",
            description ="Aurora Cluster Credentials for environment "+str(environment),
            generate_secret_string=secretsmanager.SecretStringGenerator(
                exclude_characters ="\"@/\\ '",
                generate_string_key ="password",
                password_length =30,
                secret_string_template='{"username":"'+str(aurora_cluster_username)+'"}'),
        )

        aurora_cluster_credentials = rds.Credentials.from_secret(aurora_cluster_secret, aurora_cluster_username)

        # aurora database setup
        if replica_instances < 1:
            replica_instances = 1

        aurora_serverless = rds.ServerlessCluster(
            self,
            "AuroraServerless",
            engine=rds.DatabaseClusterEngine.aurora_postgres(version=rds.AuroraPostgresEngineVersion.VER_13_6), # supports serverless 2
            backup_retention=Duration.days(backup_retention_days),
            cluster_identifier=identifier,
            credentials=aurora_cluster_credentials,
            default_database_name=identifier,
            deletion_protection=True,
            enable_data_api=True,
            parameter_group=parametergroup,
            removal_policy=RemovalPolicy.RETAIN,
            scaling=rds.ServerlessScalingOptions(
                auto_pause=Duration.minutes(5),  # default is to pause after 5 minutes of idle time
                min_capacity=rds.AuroraCapacityUnit.ACU_2,  # default is 2 Aurora capacity units (ACUs)
                max_capacity=rds.AuroraCapacityUnit.ACU_8
            ),
            security_groups=[db_security_group],
            subnet_group=db_subnet_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets
        )