pipeline {
    agent {
        node {
            label 'master'
        }
    }
    stages {
        stage('CF STEP'){
            when {
                expression { env.FLAG == 'CF' || env.FLAG == 'BOTH' }
            }
            steps {
                retry(count: 3) {
                    sh 'exit 1'
                }
            }
        }
    }
}