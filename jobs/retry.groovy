pipelineJob("retry-pipeline") {

  logRotator {
      numToKeep(10)
  }
  parameters {
    gitParam('GIT_BRANCH_NAME') {
        description 'git branch'
        type 'BRANCH'
        defaultValue 'origin/master'
        sortMode 'ASCENDING_SMART'
    }
  }
  definition {
    cpsScm {
      scm {
        git {
          remote {
                url('https://github.com/ricardocutzh/Test_repo.git')
            }
            branches('${GIT_BRANCH_NAME}')
        }
      }
      scriptPath('retry.Jenkinsfile')
      lightweight(false)
    }
  }
}