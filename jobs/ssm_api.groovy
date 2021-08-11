def create_builder_jobs(env, folder_name) {
    folder("${folder_name}/${env}") {
        description("Ottera code-generator deployment Jobs for environment ${env}")
    }
    pipelineJob("${folder_name}/${env}/code-generator") {
        description("Jenkins pipeline for code-generator")
        concurrentBuild(allowConcurrentBuild = false)
        logRotator {
            numToKeep(5)
        }
        authenticationToken("ottera-code-generator")
        parameters {
            gitParam('GIT_BRANCH_NAME') {
                description 'The Git branch to checkout'
                type 'BRANCH'
                defaultValue 'origin/master'
                sortMode 'ASCENDING_SMART'
            }
            stringParam('IDENTIFIER', 'ottera', 'identifier used in the infrastructure')
            stringParam('ENVIRONMENT', "${env}", 'environment used in the infrastructure')
            textParam('PARAMETERS_PAYLOAD', "json file", 'parameters that will be replaced in code while processing php files')
            stringParam('EXECUTION_ID', '1AB2', 'execution id')
        }
        definition {
            cpsScm {
            scm {
                git {
                remote {
                        url('https://github.com/ricardocutzh/Test_repo.git') //url("https://git-codecommit.us-west-2.amazonaws.com/v1/repos/ottera-code-generator")
                        //credentials('jenkins-codecommit-user')
                    }
                    branches('${GIT_BRANCH_NAME}')
                }
            }
            scriptPath('ssm.jenkinsfile') //scriptPath('Jenkinsfile')
            lightweight(false)
            }
        }
    }        
}

def folder_name = "Code-Generator"

folder(folder_name) {
    description('folder for Code-Generator jobs')
}

// -------------- CREATE HELPER JOBS -----------------------

// create stage jobs 
create_builder_jobs("stage", folder_name)

// create prod jobs 
create_builder_jobs("prod", folder_name)
// -------------- CREATE HELPER JOBS -----------------------