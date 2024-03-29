folder('RICARDO-TEST') {
    description('folder for general jobs')
}
// freeStyleJob('ricardo-seed-job') {
//     triggers {
//         hudsonStartupTrigger {
//             quietPeriod("10")
//             runOnChoice("ON_CONNECT")
//             label("")
//             nodeParameterName('master')
//         }
//     }

//     if( !System.getenv('DOCKER_COMPOSE') ) {
//         scm {
//             git {
//                 remote {
//                     url('https://git-codecommit.us-west-2.amazonaws.com/v1/repos/ottera-jenkins')
//                     credentials('jenkins-codecommit-user')
//                 }
//                 branches('master')
//             }
//         }
//     }

//     displayName('ricardo-seed-job')
//     steps {
//         jobDsl targets: ['jobs/*.groovy'].join('\n'),
//            removedJobAction: 'DELETE',
//            removedViewAction: 'DELETE',
//            lookupStrategy: 'SEED_JOB'
//     }

//     publishers {
//         downstreamParameterized {
//             trigger('General/seed_sharedlib') {
//                 condition('SUCCESS')
//             }
//         }

//         groovyPostBuild('''
//         import jenkins.model.Jenkins
//         import hudson.security.ACL
//         import java.util.ArrayList
//         import hudson.model.*;
//         Jenkins.instance.doQuietDown()
//         Thread.start {
//         ACL.impersonate(ACL.SYSTEM)
//         Thread.sleep(1 * 30 * 1000)
//         def q = Jenkins.instance.queue
//         for (queued in Jenkins.instance.queue.items) {
//             println queued.task.name
//             if (queued.task.name == 'General/seed_sharedlib'){
//             println 'do nothing'
//             }else{
//             q.cancel(queued.task)
//             }
//         }
//         Jenkins.instance.doCancelQuietDown()
//         }
//         ''', Behavior.DoNothing)
//     }

// }