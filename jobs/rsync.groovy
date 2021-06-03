folder('RSYNCJOBS') {
    description('rsync jobs')
}

def jobname = 'RSYNCJOBS/rsync'
pipelineJob(jobname) {

  logRotator {
      numToKeep(5)
  }
  parameters {
    gitParam('GIT_BRANCH_NAME') {
        description 'The Git branch to checkout'
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
      scriptPath('rsync.jenkinsfile')
      lightweight(false)
    }
  }
}