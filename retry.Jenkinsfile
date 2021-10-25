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
                    int count = 1
                    script {
                        try {
                            echo "${count}"
                            sh 'exit 1'
                        } catch(error) {
                            sleep  = count * 15
                            sh "sleep ${sleep}"
                            count = count + 1
                            sh 'exit 1'
                        }
                    }
                }
            }
        }
    }
}