def call (Map pipelineParams) {
    pipeline {
        agent {
            node {
                label 'master'
            }
        }
        environment {
            SSH_KEY = "test"
        }
        stages {
            stage('Started') {
                steps {
                    slackNotification('STARTED')
                }
            }
            stage('Docker Build'){
                steps {
                    echo 'Docker build'
                    sh "sleep 15"
                    sh "false"
                }
            }
        }

        post {
            always {
                echo "cleaning up..."
                slackNotification(currentBuild.result)
            }
        }
    }
}