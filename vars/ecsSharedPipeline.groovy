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
            stage('Notifying') {
                steps {
                    slackNotification(currentBuild.result)
                }
            }
            stage('Docker Build'){
                steps {
                    echo 'Docker build'
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