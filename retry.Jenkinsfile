pipeline {
    agent {
        node {
            label 'master'
        }
    }
    stages {
        stage('CF STEP'){
            steps {
                retry(count: 3) {
                    script {
                        try {
                            sh 'exit 1'
                        } catch(error) {
                            sh 'sleep 10'
                            sh 'exit 1'
                        }
                    }
                }
            }
        }
    }
}