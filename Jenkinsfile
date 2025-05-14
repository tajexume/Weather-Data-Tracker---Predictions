pipeline {
  agent any
  stages {
    stage('Clone Repo') {
      steps {
        git(url: 'https://github.com/tajexume/Weather-Data-Tracker---Predictions.git', branch: 'main')
      }
    }

    stage('') {
      steps {
        sh '''sh source .venv/Scripts/activate
sh pip install -r requirements.txt
sh python -m weather_cli --city \'San Jose\''''
      }
    }

  }
}