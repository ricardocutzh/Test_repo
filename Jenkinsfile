// #!groovy
// @Library('seed_sharedlib@master')_
// slackNotification('STARTED')
// ecsSharedPipeline(
//   ECR_REPO: '836333053777.dkr.ecr.us-west-2.amazonaws.com',
//   GIT_REPO: 'ssh://git-codecommit.us-west-2.amazonaws.com/v1/repos/ottera-stage',
//   IMAGE_NAME: 'ottera-stage',
//   TAG: 'latest',
//   REGION: 'us-west-2',
//   SITE: 'stage',
//   CHANNEL: 'zzz',
//   DEPLOY_TIMEOUT: '300'
// )
// slackNotification(currentBuild.result)
pipeline {
    agent {
        node {
            label 'master'
        }
    }
    environment {
        JENKINS_CREDS = credentials('ottera-admin')
    }
    stages {
        stage('Update Jenkins Jobs') {
            steps {
                echo "pipeline test"
            }
        }
        // stage('creating seed job') {
        //     steps {
        //         jobDsl targets: 'jobs/*.groovy', removedJobAction: 'DELETE', removedViewAction: 'DELETE'
        //         echo "test"
        //     }
        // }
        stage('Reloading Casc configuration') {
            environment {

                CRUMB = sh(script:"curl -u \"$JENKINS_CREDS_USR:$JENKINS_CREDS_PSW\" --cookie-jar ./cookie -s \"${env.JENKINS_URL}crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\\\":\\\",//crumb)\"", returnStdout: true).trim()

            }
            steps {
                sh "ls -la"
                sh "rm -rf /etc/casc/*"
                sh "ls -la /etc/casc"
                sh "cp ./casc/*.yaml /etc/casc/"
                // echo "${env.JENKINS_URL}"
                // echo "$CRUMB"
                // sh ("curl -u \"$JENKINS_CREDS_USR:$JENKINS_CREDS_PSW\" --cookie ./cookie -I -H \"${env.CRUMB}\" -X POST '${env.JENKINS_URL}configuration-as-code/reload'")

                // sh "crumb=$(curl -u \":pass\" -s '${env.JENKINS_URL}crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)')"
                // withCredentials([usernamePassword(credentialsId: 'ottera-admin', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                //     // available as an env variable, but will be masked if you try to print it out any which way
                //     // note: single quotes prevent Groovy interpolation; expansion is by Bourne Shell, which is what you want
                //     //Ssh 'echo $PASSWORD'
                //     // also available as a Groovy variable
                //     //echo USERNAME
                //     // or inside double quotes for string interpolation
                //     //echo "username is $USERNAME"

                //     //sh "crumb=\$(curl -u \"$PASSWORD:$USERNAME\" -s \"${env.JENKINS_URL}crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)\")"
                //     //sh "curl -u \"$PASSWORD:$USERNAME\" -H \"$crumb\" -X POST **${env.JENKINS_URL}configuration-as-code/reload**"
                //     environment {
                //         CRUMB = sh(script:"curl -u \"$PASSWORD:$USERNAME\" -s \"${env.JENKINS_URL}crumbIssuer/api/xml?xpath=concat(//crumbRequestField,\":\",//crumb)\"", returnStdout: true).trim()
                //     }
                // }
            }
        }
        // stage('SCRIPT CONDITION'){
        //     // when {
        //     //     expression { env.FLAG == 'DRUSH' }
        //     // }
        //     steps {
        //         echo "conditional step drush"
        //         script {
        //             if (env.FLAG == 'DRUSH' || env.FLAG == 'BOTH'){
        //                 echo "${env.FLAG}"
        //             }
        //             if (env.FLAG == 'CF' || env.FLAG == 'BOTH') {
        //                 echo "${env.FLAG}"
        //             }
        //         }
        //     }
        // }
        stage('CF STEP'){
            when {
                expression { env.FLAG == 'CF' || env.FLAG == 'BOTH' }
            }
            steps {
                echo "EXECUTED WHEN SPECIFIED, BOTH OR CF"
                echo "${env.FLAG}"
            }
        }
        stage('DRUSH STEP'){
            when {
                expression { env.FLAG == 'DRUSH' || env.FLAG == 'BOTH' }
            }
            steps {
                echo "EXECUTED WHEN SPECIFIED, BOTH OR DRUSH"
                echo "${env.FLAG}"
            }
        }
    }
}