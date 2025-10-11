// Jenkinsfile (Declarative Pipeline) - pytest + Docker build & push + junit reporting
pipeline {
  agent any

  environment {
    IMAGE_BASE = "swenforgets/scientific-calculator"   // <--- change this
    DOCKERHUB_CRED_ID = "dockerhub-creds"                         // <--- Jenkins credential id (username/password)
    VENV_DIR = "venv"
  }

  options {
    // keep build logs for 30 days, and allow 50 builds to be kept
    buildDiscarder(logRotator(daysToKeepStr: '30', numToKeepStr: '50'))
    timestamps()
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Diagnostics') {
      steps {
        sh """
          echo '===== Workspace root:'
          pwd
          echo '===== List root:'
          ls -la
          echo '===== Show Docker binary (if present):'
          which docker || true
          echo '===== Docker version:'
          docker --version || true
          echo '===== Docker info (may require permissions):'
          docker info || true
          echo '===== Disk free:'
          df -h
        """
      }
    }

    stage('Install Dependencies & Run Tests') {
      steps {
        sh '''
        set -eux

        # remove previous venv to avoid permission problems
        rm -rf venv || true

        # create venv
        python3 -m venv venv

        # upgrade pip/setuptools/wheel using venv python
        ./venv/bin/python -m pip install --upgrade pip setuptools wheel

        # install requirements
        ./venv/bin/pip install --no-cache-dir -r requirements.txt

        # run pytest using venv python
        ./venv/bin/pytest -v --maxfail=1 --disable-warnings --junitxml=reports/results.xml
        '''
      }
      post {
        always {
          junit allowEmptyResults: true, testResults: 'reports/results.xml'
          archiveArtifacts artifacts: 'reports/**', allowEmptyArchive: true
        }
      }
    }


    stage('Build Docker Image') {
      steps {
        script {
          sh "docker build -t ${IMAGE_BASE}:${BUILD_NUMBER} ."
        }
      }
    }

    stage('Docker Login & Push') {
      steps {
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
      sh '''
        echo "Build complete. IMAGE=${IMAGE_BASE}:${BUILD_NUMBER}"
      '''
    }
  }
}
