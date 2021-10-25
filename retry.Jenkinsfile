int count = 0
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
                            echo "${count}"
                            sh 'exit 1'
                        } catch(error) {
                            sh 'sleep 10'
                            count = count + 1
                            sh 'exit 1'
                        }
                    }
                }
            }
        }
    }
}