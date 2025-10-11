// Jenkinsfile (Declarative Pipeline) - pytest + Docker build & push + junit reporting
pipeline {
  agent any

  environment {
    IMAGE_BASE = "swenforgets/scientific-calculator"   // <--- change this
    DOCKERHUB_CRED_ID = "dockerhub-creds"                         // <--- Jenkins credential id (username/password)
    VENV_DIR = "venv"
  }

  options {
    // keep build logs for 30 days, and allow 5 concurrent builds
    buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '50'))
    timestamps()
    ansiColor('xterm')
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Install Dependencies & Run Tests') {
      steps {
        script {
          // create venv, install dependencies, run pytest with junit xml output
          sh """
            python3 -m venv ${VENV_DIR} || true
            . ${VENV_DIR}/bin/activate
            pip install --upgrade pip
            pip install -r requirements.txt
            mkdir -p reports
            pytest -v --maxfail=1 --disable-warnings --junitxml=reports/results.xml
          """
        }
      }
      post {
        always {
          // Archive pytest XML (JUnit) so Jenkins can show test results
          junit allowEmptyResults: true, testResults: 'reports/results.xml'
          archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
      }
    }

    stage('Build Docker Image') {
      steps {
        script {
          // Build with a BUILD_NUMBER tag for traceability
          sh "docker build -t ${IMAGE_BASE}:${BUILD_NUMBER} ."
        }
      }
    }

    stage('Docker Login & Push') {
      steps {
        // login and push using stored Jenkins credentials
        withCredentials([usernamePassword(credentialsId: env.DOCKERHUB_CRED_ID, usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
          sh '''
            echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
            docker tag ${IMAGE_BASE}:${BUILD_NUMBER} ${IMAGE_BASE}:latest
            docker push ${IMAGE_BASE}:${BUILD_NUMBER}
            docker push ${IMAGE_BASE}:latest
          '''
        }
      }
    }

    stage('Deploy (optional)') {
      when {
        expression { return env.DEPLOY == 'true' || currentBuild.currentResult == 'SUCCESS' }
      }
      steps {
        echo "Deployment step is optional — add your deploy commands here (Ansible / kubectl / ssh)."
      }
    }
  }

  post {
    success {
      echo "Pipeline succeeded: built and pushed ${IMAGE_BASE}:${BUILD_NUMBER}"
    }
    unstable {
      echo "Pipeline unstable — there were test failures or warnings."
    }
    failure {
      echo "Pipeline failed. Check console output and test reports."
    }
    always {
      // print a short summary and clean up local dangling images optionally
      sh '''
        echo "Build complete. IMAGE=${IMAGE_BASE}:${BUILD_NUMBER}"
        # optional cleanup - uncomment if you want Jenkins agent to remove images after push
        # docker rmi ${IMAGE_BASE}:${BUILD_NUMBER} || true
      '''
    }
  }
}
