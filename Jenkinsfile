pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('Create VENV') {
      steps {
        sh '''python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
'''
      }
    }

    stage('Run Script') {
      steps {
        sh '''source venv/bin/activate
python your_script.py
'''
      }
    }

  }
}